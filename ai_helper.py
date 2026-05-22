"""
ai_helper.py — Google Gemini AI integration (google-genai SDK).

Critical fixes in this revision:
  • ✅ Updated model chain: gemini-2.5-flash → gemini-2.5-flash-lite → gemini-2.0-flash
    (gemini-1.5-* is shut down and returns 404)
  • ✅ Cached working model — once we find one that works, stop trying others
  • ✅ NO MORE SILENT FALLBACKS — actual API errors are surfaced to the user
  • ✅ test_connection() — verify the API key and find a working model
  • ✅ chat_stream() — streaming chat responses for ChatGPT-style UX
  • ✅ Last error stored in session_state for diagnostics
"""

from __future__ import annotations
import os
from typing import Generator
import streamlit as st


# ──────────────────────────────────────────────────────────────
# MODEL CHAIN
# Order matters: try newest/cheapest first, fall back if 404 / quota.
# ──────────────────────────────────────────────────────────────

MODEL_CHAIN: list[str] = [
    "gemini-2.5-flash",        # Current stable — recommended default
    "gemini-2.5-flash-lite",   # Cheaper / faster fallback
    "gemini-2.0-flash",        # Sunset June 2026 but still works
]


# ──────────────────────────────────────────────────────────────
# KEY & CLIENT MANAGEMENT
# ──────────────────────────────────────────────────────────────

def _resolve_api_key() -> str:
    """Resolve API key from session_state, then env var."""
    key = (st.session_state.get("gemini_api_key") or "").strip()
    if key:
        return key
    env_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if env_key:
        st.session_state["gemini_api_key"] = env_key
        return env_key
    return ""


def get_client():
    """Return a cached Gemini client, or None if no key/SDK."""
    api_key = _resolve_api_key()
    if not api_key:
        return None

    cached_key = st.session_state.get("_gemini_cached_key")
    cached = st.session_state.get("_gemini_client")
    if cached is not None and cached_key == api_key:
        return cached

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        st.session_state["_gemini_cached_key"] = api_key
        st.session_state["_gemini_client"] = client
        # Reset working model when key changes
        st.session_state.pop("_gemini_working_model", None)
        st.session_state.pop("_gemini_last_error", None)
        return client
    except ImportError:
        st.session_state["_gemini_last_error"] = (
            "The `google-genai` package is not installed. Run: "
            "`pip install google-genai`"
        )
        return None
    except Exception as e:
        st.session_state["_gemini_last_error"] = f"Failed to create client: {e}"
        return None


def get_active_model() -> str:
    """Return the currently working model, or the first untried candidate."""
    return st.session_state.get("_gemini_working_model") or MODEL_CHAIN[0]


def get_last_error() -> str:
    """Return the most recent actual API error, or empty string."""
    return st.session_state.get("_gemini_last_error", "") or ""


# ──────────────────────────────────────────────────────────────
# CORE CALL — surfaces real errors
# ──────────────────────────────────────────────────────────────

class GeminiError(Exception):
    """Raised when every model in the chain fails."""


def _generate(prompt: str, *, model: str | None = None) -> str:
    """
    Call Gemini and return text. Raises GeminiError with a clear,
    real error message if every model in the chain fails.
    """
    client = get_client()
    if client is None:
        err = get_last_error() or "No Gemini API key set."
        raise GeminiError(err)

    # Build the candidate list: working model first if known, then the rest
    working = st.session_state.get("_gemini_working_model")
    if model:
        candidates = [model]
    elif working:
        candidates = [working] + [m for m in MODEL_CHAIN if m != working]
    else:
        candidates = list(MODEL_CHAIN)

    errors: list[str] = []
    for candidate in candidates:
        try:
            response = client.models.generate_content(
                model=candidate,
                contents=prompt,
            )
            text = (getattr(response, "text", "") or "").strip()
            if text:
                # Cache this working model
                st.session_state["_gemini_working_model"] = candidate
                st.session_state["_gemini_last_error"] = ""
                return text
            errors.append(f"{candidate}: empty response")
        except Exception as e:
            msg = str(e).splitlines()[0][:240] if str(e) else "unknown error"
            errors.append(f"{candidate}: {msg}")
            continue

    full_err = " | ".join(errors)
    st.session_state["_gemini_last_error"] = full_err
    raise GeminiError(full_err)


def _safe_generate(prompt: str, fallback_label: str = "[AI unavailable]") -> str:
    """
    Convenience wrapper that returns a clearly-labelled error string
    instead of raising — for UI code that doesn't want try/except.
    The error is ALWAYS visible (not silently hidden).
    """
    try:
        return _generate(prompt)
    except GeminiError as e:
        return f"⚠️ AI request failed — {e}\n\n_{fallback_label}_"


# ──────────────────────────────────────────────────────────────
# CONNECTION TEST
# ──────────────────────────────────────────────────────────────

def test_connection() -> tuple[bool, str, str]:
    """Verify the API key works. Returns (success, model_name, message)."""
    if not _resolve_api_key():
        return (False, "", "No API key set. Paste your key in the sidebar.")

    client = get_client()
    if client is None:
        return (False, "", get_last_error() or "Could not initialize client.")

    last_err = ""
    for candidate in MODEL_CHAIN:
        try:
            response = client.models.generate_content(
                model=candidate,
                contents="Reply with exactly the word: OK",
            )
            text = (getattr(response, "text", "") or "").strip()
            if text:
                st.session_state["_gemini_working_model"] = candidate
                st.session_state["_gemini_last_error"] = ""
                return (True, candidate, f"Connected — using {candidate}")
        except Exception as e:
            last_err = f"{candidate}: {str(e).splitlines()[0][:200]}"
            continue

    return (False, "", f"All models failed. Last error → {last_err}")


# ──────────────────────────────────────────────────────────────
# STREAMING (for chat UX)
# ──────────────────────────────────────────────────────────────

def stream_generate(prompt: str) -> Generator[str, None, None]:
    """
    Yield text chunks from Gemini as they arrive (ChatGPT-style streaming).
    Falls back to non-streaming if the SDK doesn't support streaming.
    """
    client = get_client()
    if client is None:
        err = get_last_error() or "No Gemini API key set."
        yield f"⚠️ {err}"
        return

    active = get_active_model()
    candidates = [active] + [m for m in MODEL_CHAIN if m != active]

    last_err = ""
    for candidate in candidates:
        try:
            stream = client.models.generate_content_stream(
                model=candidate,
                contents=prompt,
            )
            any_text = False
            for chunk in stream:
                chunk_text = getattr(chunk, "text", "") or ""
                if chunk_text:
                    any_text = True
                    yield chunk_text
            if any_text:
                st.session_state["_gemini_working_model"] = candidate
                st.session_state["_gemini_last_error"] = ""
                return
        except Exception as e:
            last_err = f"{candidate}: {str(e).splitlines()[0][:200]}"
            continue

    # Last resort
    try:
        text = _generate(prompt)
        yield text
    except GeminiError as e:
        yield f"⚠️ AI request failed — {e or last_err}"


def chat_stream(messages: list[dict]) -> Generator[str, None, None]:
    """
    Stream a chat response given a message history.
    `messages`: list of {"role": "user"|"assistant"|"system", "content": str}.
    """
    parts = []
    system_msgs = [m["content"] for m in messages if m.get("role") == "system" and m.get("content", "").strip()]
    if system_msgs:
        parts.append("System instructions:\n" + "\n".join(system_msgs))
        parts.append("")

    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role == "system" or not content.strip():
            continue
        label = "User" if role == "user" else "Assistant"
        parts.append(f"{label}: {content}")

    parts.append("Assistant:")
    prompt = "\n\n".join(parts)
    yield from stream_generate(prompt)


# ──────────────────────────────────────────────────────────────
# TASK HELPERS
# ──────────────────────────────────────────────────────────────

def paraphrase_text(text: str) -> str:
    if not text or not text.strip():
        return text
    prompt = (
        "Paraphrase the following text. Keep the same meaning but use "
        "different wording, sentence structure, and natural phrasing. "
        "Output ONLY the paraphrased text — no headings, labels, or "
        "explanations.\n\n"
        f"{text}"
    )
    return _safe_generate(prompt, fallback_label="paraphrase failed")


def build_paraphrased_content(content: list) -> list:
    result = []
    for item in content:
        original = item.get("text", "")
        paraphrased = paraphrase_text(original) if original.strip() else original
        result.append({**item, "paraphrased": paraphrased})
    return result


def generate_content(prompt: str) -> str:
    if not prompt or not prompt.strip():
        return "Please enter a prompt."
    system = (
        "You are a professional content writer. Write well-structured, "
        "engaging content based on the user's prompt. Use clear ## headings, "
        "well-formed paragraphs, and bullet points where appropriate. "
        "Output ONLY the content — no preamble like 'Here is...' or 'Sure!'."
    )
    full_prompt = f"{system}\n\nUser prompt: {prompt}"
    return _safe_generate(full_prompt, fallback_label="content generation failed")


def enhance_text(text: str) -> str:
    if not text or not text.strip():
        return text
    prompt = (
        "You are an expert editor. Improve the following text by:\n"
        "1. Fixing all grammar and spelling mistakes\n"
        "2. Improving sentence clarity and flow\n"
        "3. Making it more professional and readable\n\n"
        "Preserve the author's intent and tone. Output ONLY the improved "
        "text — no explanations.\n\n"
        f"{text}"
    )
    return _safe_generate(prompt, fallback_label="enhancement failed")


def grammar_check_detailed(text: str) -> str:
    if not text or not text.strip():
        return "No text provided."
    prompt = (
        "Analyze the following text for grammar, spelling, and writing issues. "
        "For each issue, list: (a) the original phrase, (b) what is wrong, "
        "(c) the correction. Use Markdown bullets. Then provide the fully "
        "corrected text under a `## Corrected Text` heading.\n\n"
        f"{text}"
    )
    return _safe_generate(prompt, fallback_label="grammar audit failed")


def summarize_text(text: str, style: str = "concise") -> str:
    if not text or not text.strip():
        return text
    style_map = {
        "concise":  "Write a concise 2-3 sentence summary.",
        "detailed": "Write a detailed summary covering all key points, organized into 2-3 short paragraphs.",
        "bullet":   "Summarize as 5 clear, parallel bullet points.",
        "tldr":     "Write a one-sentence TL;DR.",
    }
    instruction = style_map.get(style, style_map["concise"])
    prompt = f"{instruction} Output ONLY the summary.\n\n{text}"
    return _safe_generate(prompt, fallback_label="summary failed")


def explain_research_abstract(title: str, abstract: str) -> str:
    prompt = (
        f"Paper title: {title}\n\n"
        f"Abstract:\n{abstract}\n\n"
        "Explain this research paper abstract in plain, simple English so "
        "a curious non-specialist can understand it. Use this structure:\n"
        "**Problem:** what does it try to solve\n"
        "**Approach:** how does it solve it\n"
        "**Why it matters:** the practical impact\n\n"
        "Output ONLY the explanation."
    )
    return _safe_generate(prompt, fallback_label="explanation failed")


def ai_summarize_topic(topic: str, raw_content: str) -> str:
    if not raw_content or not raw_content.strip():
        return raw_content
    prompt = (
        f"Topic: {topic}\n\n"
        f"Raw content from web sources:\n{raw_content[:6000]}\n\n"
        "Write a clear, well-structured overview of the topic using the "
        "content above as reference. Use ## headings, paragraphs, and bullet "
        "points where helpful. Cover: introduction, key concepts, applications, "
        "and significance. Output ONLY the structured overview."
    )
    return _safe_generate(prompt, fallback_label="topic overview failed")


def extract_keywords(text: str, n: int = 8) -> list[str]:
    if not text or not text.strip():
        return []
    prompt = (
        f"Extract the {n} most important keywords or key phrases from the "
        "text below. Output them as a comma-separated list, nothing else. "
        "Do not number them. Do not add quotes.\n\n"
        f"{text[:4000]}"
    )
    raw = _safe_generate(prompt, fallback_label="keywords failed")
    if raw.startswith("⚠️"):
        return []
    parts = [p.strip(" .•-*\"'") for p in raw.replace("\n", ",").split(",")]
    return [p for p in parts if p][:n]


def detect_language_and_topic(text: str) -> dict:
    if not text or not text.strip():
        return {"language": "Unknown", "topic": "Unknown"}
    prompt = (
        "For the text below, detect:\n"
        "1. The language (English name only, e.g. 'English', 'Spanish')\n"
        "2. The main topic in 3-6 words\n\n"
        "Output strictly in this format on two lines:\n"
        "Language: <name>\n"
        "Topic: <topic>\n\n"
        f"Text:\n{text[:1500]}"
    )
    raw = _safe_generate(prompt, fallback_label="detection failed")
    result = {"language": "Unknown", "topic": "Unknown"}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip().lower()
        v = v.strip()
        if k.startswith("language") and v and not v.startswith("⚠"):
            result["language"] = v
        elif k.startswith("topic") and v and not v.startswith("⚠"):
            result["topic"] = v
    return result


def smart_pipeline_summary(text: str) -> dict:
    return {
        "summary":     summarize_text(text, style="detailed"),
        "tldr":        summarize_text(text, style="tldr"),
        "keywords":    extract_keywords(text, n=8),
        "meta":        detect_language_and_topic(text),
        "paraphrased": paraphrase_text(text[:3000]),
    }


# ──────────────────────────────────────────────────────────────
# SIDEBAR API KEY WIDGET (with connection test)
# ──────────────────────────────────────────────────────────────

def render_api_key_sidebar():
    with st.sidebar:
        st.markdown(
            "<div style='padding: 0.5rem 0;'>"
            "<h3 style='color:#a78bfa; margin:0; font-weight:700;'>🔑 Gemini AI Key</h3>"
            "</div>",
            unsafe_allow_html=True,
        )

        key = st.text_input(
            "Enter API Key",
            type="password",
            value=st.session_state.get("gemini_api_key", ""),
            placeholder="AIza...",
            help="Get a free key at https://aistudio.google.com/app/apikey",
            key="gemini_key_input",
            label_visibility="collapsed",
        )
        if key and key != st.session_state.get("gemini_api_key"):
            st.session_state["gemini_api_key"] = key
            st.session_state.pop("_gemini_client", None)
            st.session_state.pop("_gemini_cached_key", None)
            st.session_state.pop("_gemini_working_model", None)

        # Status
        if not _resolve_api_key():
            st.markdown('<div class="status-pill warning">⚠ No key set</div>', unsafe_allow_html=True)
        else:
            working = st.session_state.get("_gemini_working_model")
            if working:
                st.markdown(
                    f'<div class="status-pill success">✓ {working}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div class="status-pill warning">● Untested — click below</div>',
                    unsafe_allow_html=True,
                )

        if st.button("🔌 Test Connection", use_container_width=True, key="sidebar_test_conn"):
            with st.spinner("Testing..."):
                ok, model, msg = test_connection()
            if ok:
                st.success(f"✅ {msg}")
            else:
                st.error(f"❌ {msg}")

        st.caption("[Get a free key →](https://aistudio.google.com/app/apikey)")
        st.markdown("---")
        st.markdown(
            "<div style='font-size: 0.78rem; color: #94a3b8; line-height: 1.5;'>"
            "<b style='color:#cbd5e1;'>Free tier limits</b><br>"
            "• 15 requests / minute<br>"
            "• 1M tokens / day"
            "</div>",
            unsafe_allow_html=True,
        )

        last_err = get_last_error()
        if last_err:
            with st.expander("⚠️ Last error", expanded=False):
                st.code(last_err, language="text")

        st.markdown("---")
