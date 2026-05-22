# 🧠 AI Content Intelligence Platform

A unified Streamlit workspace with **chat, scraping, analyzing, paraphrasing, and content generation** — fully automated end-to-end with **Google Gemini 2.5 Flash**.

---

🚀 Live Project Link: 
https://content-intelligence-platform.streamlit.app/

## ✨ What's New (v3 — this revision)

### 🐛 Critical Bugs Fixed
- **`gemini-1.5-flash` was returning 404** — Google retired all Gemini 1.5 models on Apr 22, 2026. Updated model chain to current stable: `gemini-2.5-flash` → `gemini-2.5-flash-lite` → `gemini-2.0-flash`.
- **Silent failures** — previous code hid every API error behind a fallback string. Now **all errors are surfaced** in clearly-styled red boxes so you can actually debug.
- **Invisible dropdown text** in Content Generator (Tone / Length / Audience boxes appeared empty) — fixed CSS targeting BaseWeb selectbox internals.
- **`yasterday` not caught** by Quick Grammar Fix — expanded the spelling map with 50+ new entries.
- **Grammar fix wasn't using AI** even when key was set — Text Intelligence now prioritizes AI when connected, rules-only as fallback.

### 🆕 New Chat Module
A full **ChatGPT/Claude-style chat interface** as the headline page:
- ✅ **Streaming responses** — tokens appear as they're generated
- ✅ **Conversation history** persists for the session
- ✅ **Custom system prompt** — set the AI's persona (tutor, coder, writer, coach, etc.)
- ✅ **7 pre-built personas** + custom mode
- ✅ **Export conversation** as Word document
- ✅ **New Chat / Clear** buttons

### 🔌 Connection Test
- New **Test Connection button** in both sidebar and home page — verifies the API key works and tells you exactly which model it picked.
- Working model is cached so subsequent calls don't keep retrying.

---

## 📋 Prerequisites

- Python **3.9+**
- pip
- A free **Gemini API key** from https://aistudio.google.com/app/apikey

---

## 🛠️ Setup

### 1. Install dependencies

```cmd
pip install -r requirements.txt
```

If `pip` isn't recognized on Windows, use `python -m pip install -r requirements.txt`.

### 2. (Optional) Set your API key as an env variable

```cmd
:: Windows CMD
set GEMINI_API_KEY=AIza...

:: Windows PowerShell
$env:GEMINI_API_KEY = "AIza..."

# macOS / Linux
export GEMINI_API_KEY="AIza..."
```

### 3. Run the app

```cmd
streamlit run Home.py
```

If `streamlit` isn't recognized as a command, run it through Python instead:

```cmd
python -m streamlit run Home.py
```

The app opens at https://content-intelligence-platform.streamlit.app/.

---

## 🗂️ Project Structure

```
Final_Project_AI/
├── Home.py                            ← Landing page + Test Connection
├── ai_helper.py                       ← Gemini AI integration (current models, no silent errors)
├── scraper.py                         ← Web scraping utilities
├── styles.py                          ← Centralized CSS / theme + chat bubbles + error boxes
├── requirements.txt                   ← Dependencies
├── .streamlit/
│   └── config.toml                    ← Dark theme config
├── pages/
│   ├── 0_💬_AI_Chat.py                ← NEW — ChatGPT-style chat interface
│   ├── 1_🌐_URL_Scraper.py            ← URL → AI paraphrase + summary + keywords
│   ├── 2_🔍_Topic_Retrieval.py        ← Multi-source fetch + AI overview
│   ├── 3_🧠_Text_Intelligence.py      ← Grammar fix + AI enhancement + metrics
│   ├── 4_📚_Research_Assistant.py     ← arXiv search + plain-English explanation
│   ├── 5_✍️_Content_Generator.py      ← Prompt → fresh AI content
│   └── 6_🎯_Smart_Pipeline.py         ← Full automation
└── README.md
```

---

## ❓ Troubleshooting

| Problem | Fix |
|---------|-----|
| `'streamlit' is not recognized as an internal or external command` | Run `python -m streamlit run Home.py` instead |
| `ModuleNotFoundError: No module named 'google.genai'` | Run `pip install google-genai` (note: NOT `google-generativeai`) |
| AI features show "AI request failed" | Click **🔌 Test Connection** in the sidebar — if it fails, the error message will tell you exactly why (bad key, rate limit, etc.) |
| `404 NOT_FOUND` for a model | Your version is using a retired model. Update by re-downloading this project. |
| `429` rate limit | Free-tier limit is 15 req/min — wait 60 seconds and retry |
| `API key not valid` | Verify the key at aistudio.google.com/app/apikey |
| Sidebar emoji icons not showing | Make sure files saved with UTF-8 encoding |

---

## 🤖 Active Model Chain

```
1. gemini-2.5-flash         ← preferred (fast, capable, current)
2. gemini-2.5-flash-lite    ← cheaper fallback
3. gemini-2.0-flash         ← legacy fallback (sunset June 2026)
```

The app automatically tries them in order. The first one that succeeds is cached for the rest of your session.

---

## 🔒 Security Note

This project does **not** hardcode any API key in source code. The key is read from:

1. The sidebar input field (per-session, in-memory only), or
2. The `GEMINI_API_KEY` environment variable

Nothing is logged or persisted to disk.
