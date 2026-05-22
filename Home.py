"""
Home.py — Landing page for the AI Content Intelligence Platform.

Updated to:
  • Advertise the new Chat module
  • Show the live model status
  • Provide the connection test button right on the home page
"""

import os
import streamlit as st
from ai_helper import render_api_key_sidebar, _resolve_api_key, test_connection
from styles import inject_css, gradient_divider



# PAGE CONFIG

st.set_page_config(
    page_title="AI Intelligent Web Scraper Platform",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="expanded",
)

inject_css()



# API KEY (loaded from env var or empty by default)


if "gemini_api_key" not in st.session_state:
    st.session_state["gemini_api_key"] = os.environ.get("GEMINI_API_KEY", "")

render_api_key_sidebar()


st.markdown(
    """
    <div style="text-align: center; padding: 2rem 0 1rem 0;">
        <div class="hero-badge floating">⚡ Powered by Google Gemini 2.5 Flash</div>
        <h1 style="font-size: 3.5rem; margin: 0.5rem 0;">
            AI Content Intelligence
        </h1>
        <p class="hero-subtitle" style="margin: 0.6rem auto 0 auto;">
            A unified workspace with chat, scraping, analysis, paraphrasing,
            and content generation — fully automated end-to-end with real AI.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


key_set = bool(_resolve_api_key())
working_model = st.session_state.get("_gemini_working_model")

c_status, c_btn, _ = st.columns([2, 1, 1])
with c_status:
    if not key_set:
        st.markdown(
            '<div style="text-align:left; margin-top:0.4rem;">'
            '<span class="status-pill warning">● Add your API key in the sidebar to begin</span>'
            '</div>',
            unsafe_allow_html=True,
        )
    elif working_model:
        st.markdown(
            f'<div style="text-align:left; margin-top:0.4rem;">'
            f'<span class="status-pill success">● Active model: {working_model}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="text-align:left; margin-top:0.4rem;">'
            '<span class="status-pill warning">● Key set — click "Test Connection" to verify it works</span>'
            '</div>',
            unsafe_allow_html=True,
        )

with c_btn:
    if st.button("🔌 Test Connection", use_container_width=True, disabled=not key_set):
        with st.spinner("Testing your API key..."):
            ok, model, msg = test_connection()
        if ok:
            st.success(f"✅ {msg}")
            st.rerun()
        else:
            st.error(f"❌ {msg}")

gradient_divider()





st.markdown("### 🎯 Modules")
st.caption("Each module is independent — use them in any order, or chain them through Smart Pipeline.")
st.write("")

modules = [
    ("💬", "AI Chat",            "Real conversation with Gemini — streaming responses, message history, custom personas.",   "#22d3ee"),
    ("🌐", "URL Scraper",        "Extract content from any URL. AI paraphrases it into fresh text and exports to Word.",      "#6366f1"),
    ("🔍", "Topic Retrieval",    "Pull info on any topic from Wikipedia, Britannica & more. AI writes a structured overview.","#a78bfa"),
    ("🧠", "Text Intelligence",  "Grammar fix, readability metrics, sentiment, keywords, and full AI text enhancement.",      "#f472b6"),
    ("📚", "Research Assistant", "Search real papers from arXiv. AI explains complex abstracts in plain English.",            "#fbbf24"),
    ("✍️", "Content Generator",  "Generate stories, essays, explanations from any prompt with adjustable tone and length.",   "#fb923c"),
    ("🎯", "Smart Pipeline",     "One-click full automation: scrape → analyze → paraphrase → keywords → summary → export.",   "#10b981"),
]

# Render in rows of 3
for row_start in (0, 3, 6):
    row_modules = modules[row_start:row_start + 3]
    if not row_modules:
        break
    cols = st.columns(3, gap="medium")
    for col, (icon, title, desc, color) in zip(cols, row_modules):
        with col:
            st.markdown(
                f"""
                <div class="glass-card" style="height: 100%; min-height: 175px;">
                    <div class="feature-icon" style="filter: drop-shadow(0 0 14px {color}80);">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

gradient_divider()



# AI PIPELINE VISUALIZATION


st.markdown("### 🤖 How the AI Pipeline Works")
st.caption("From input to download — every module follows this same pattern.")
st.write("")

steps = [
    ("1", "Input",         "URL, topic, text, prompt, or chat"),
    ("2", "Extraction",    "Scrape, fetch, or read"),
    ("3", "AI Processing", "Gemini 2.5 Flash analysis"),
    ("4", "AI Generation", "Paraphrase, enhance, write, chat"),
    ("5", "Export",        "Word docx · Markdown · TXT"),
]

cols = st.columns(5, gap="small")
for col, (num, title, desc) in zip(cols, steps):
    with col:
        st.markdown(
            f"""
            <div class="pipeline-step">
                <div class="step-num">{num}</div>
                <div class="step-title">{title}</div>
                <div class="step-desc">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

gradient_divider()


# ─────────────────────────────────────────────
# QUICK START
# ─────────────────────────────────────────────

c1, c2 = st.columns([1.2, 1], gap="large")

with c1:
    st.markdown("### 🚀 Quick Start")
    st.markdown(
        """
        1. **Get a free Gemini API key** at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
        2. **Paste it** into the sidebar on the left
        3. Click **🔌 Test Connection** to verify it works
        4. **Pick a module** from the sidebar nav and start working
        5. **Or jump to AI Chat** for a ChatGPT-style conversation

        Every module supports downloading results as `.docx` files.
        Free Gemini tier: **15 requests/min**, **1M tokens/day** — more than enough.
        """
    )

with c2:
    st.markdown("### 💡 What's New")
    st.markdown(
        """
        - 💬 **AI Chat module** — full conversation with streaming
        - 🤖 Updated to **Gemini 2.5 Flash** (Gemini 1.5 was retired)
        - 🚦 **Test Connection** button verifies your key actually works
        - 🐛 Real error messages now visible (no more silent failures)
        - 🎨 Fixed dropdown text visibility in dark theme
        - 📚 Expanded grammar dictionary (catches "yasterday" etc.)
        """
    )

gradient_divider()

st.markdown(
    """
    <div style="text-align:center; color: #64748b; font-size: 0.85rem; padding: 1rem 0 2rem 0;">
        <span style="background: linear-gradient(135deg, #a78bfa, #22d3ee); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700;">
            AI Content Intelligence Platform
        </span>
        &nbsp;·&nbsp; Built with Streamlit &amp; Python &nbsp;·&nbsp; Powered by Google Gemini 2.5 Flash
    </div>
    """,
    unsafe_allow_html=True,
)
