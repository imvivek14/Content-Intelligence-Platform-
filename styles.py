"""
styles.py — Centralized CSS / theme module for the AI Content Intelligence Platform.

Modern dark theme with:
  • Glassmorphism cards
  • Gradient accents (indigo / purple / cyan)
  • Smooth hover animations
  • Custom button & input styling
  • Animated hero section
"""

import streamlit as st


CUSTOM_CSS = """
<style>
/* ───────────────── GLOBAL FONT & BASE ───────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* ───────────────── APP BACKGROUND ───────────────── */
.stApp {
    background:
        radial-gradient(circle at 15% 20%, rgba(99, 102, 241, 0.18) 0%, transparent 45%),
        radial-gradient(circle at 85% 75%, rgba(168, 85, 247, 0.15) 0%, transparent 45%),
        radial-gradient(circle at 50% 50%, rgba(34, 211, 238, 0.08) 0%, transparent 60%),
        linear-gradient(135deg, #0a0a1a 0%, #0f0f23 50%, #0a0a1a 100%);
    background-attachment: fixed;
    color: #e2e8f0;
}

/* Hide default Streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ───────────────── SIDEBAR ───────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(15, 15, 35, 0.95) 0%, rgba(10, 10, 26, 0.98) 100%);
    border-right: 1px solid rgba(99, 102, 241, 0.15);
    backdrop-filter: blur(20px);
}

[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p {
    color: #cbd5e1 !important;
}

/* ───────────────── HEADINGS ───────────────── */
h1 {
    font-weight: 800 !important;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #a78bfa 0%, #818cf8 50%, #22d3ee 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1 !important;
}

h2, h3, h4 {
    color: #f1f5f9 !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em;
}

/* ───────────────── BUTTONS ───────────────── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: #ffffff !important;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
    font-size: 0.95rem;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow:
        0 4px 14px 0 rgba(99, 102, 241, 0.35),
        inset 0 1px 0 rgba(255, 255, 255, 0.15);
    letter-spacing: 0.01em;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow:
        0 8px 24px 0 rgba(99, 102, 241, 0.5),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
    background: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%);
}

.stButton > button:active {
    transform: translateY(0);
}

.stButton > button:disabled {
    background: rgba(71, 85, 105, 0.4) !important;
    color: rgba(203, 213, 225, 0.5) !important;
    box-shadow: none;
    cursor: not-allowed;
}

/* Primary button gets a brighter gradient */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 50%, #f59e0b 100%);
    box-shadow: 0 4px 18px 0 rgba(236, 72, 153, 0.4);
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #a78bfa 0%, #f472b6 50%, #fbbf24 100%);
    box-shadow: 0 8px 28px 0 rgba(236, 72, 153, 0.55);
}

/* Download buttons match secondary style */
.stDownloadButton > button {
    background: linear-gradient(135deg, rgba(34, 211, 238, 0.85) 0%, rgba(99, 102, 241, 0.85) 100%) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.25s ease !important;
    border: none !important;
}

.stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(34, 211, 238, 0.4);
}

/* ───────────────── INPUTS ───────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: rgba(30, 30, 60, 0.5) !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
    border-radius: 12px !important;
    color: #f1f5f9 !important;
    padding: 0.65rem 1rem !important;
    transition: all 0.2s ease;
    font-size: 0.95rem !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stNumberInput > div > div > input:focus {
    border-color: rgba(168, 85, 247, 0.6) !important;
    box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.15) !important;
    background: rgba(30, 30, 60, 0.7) !important;
}

.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: rgba(148, 163, 184, 0.6) !important;
}

/* SELECTBOX — make selected value text visible (the bug from screenshot 1) */
.stSelectbox [data-baseweb="select"],
.stSelectbox [data-baseweb="select"] > div,
.stSelectbox [data-baseweb="select"] div[role="combobox"],
.stSelectbox [data-baseweb="select"] span,
.stSelectbox [data-baseweb="select"] input {
    color: #f1f5f9 !important;
    background-color: transparent !important;
}

.stSelectbox [data-baseweb="select"] {
    background: rgba(30, 30, 60, 0.5) !important;
    border-radius: 12px !important;
}

/* Dropdown popover (the option list when opened) */
[data-baseweb="popover"] [role="listbox"],
[data-baseweb="menu"] {
    background: rgba(15, 15, 35, 0.98) !important;
    border: 1px solid rgba(168, 85, 247, 0.4) !important;
    border-radius: 12px !important;
}

[data-baseweb="popover"] [role="option"],
[data-baseweb="menu"] li {
    color: #e2e8f0 !important;
    background: transparent !important;
}

[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="menu"] li:hover {
    background: rgba(99, 102, 241, 0.25) !important;
    color: #ffffff !important;
}

/* Radio buttons (used in Smart Pipeline) */
.stRadio [role="radiogroup"] label {
    color: #e2e8f0 !important;
}

/* Slider */
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: linear-gradient(135deg, #a78bfa, #22d3ee) !important;
}

/* Checkbox */
.stCheckbox label {
    color: #cbd5e1 !important;
}

/* ───────────────── METRICS ───────────────── */
[data-testid="stMetric"] {
    background: rgba(30, 30, 60, 0.4);
    border: 1px solid rgba(99, 102, 241, 0.18);
    border-radius: 16px;
    padding: 1.2rem 1rem;
    backdrop-filter: blur(12px);
    transition: all 0.3s ease;
}

[data-testid="stMetric"]:hover {
    border-color: rgba(168, 85, 247, 0.5);
    transform: translateY(-3px);
    box-shadow: 0 12px 28px -10px rgba(99, 102, 241, 0.4);
}

[data-testid="stMetricValue"] {
    color: #f1f5f9 !important;
    font-weight: 700 !important;
    font-size: 1.5rem !important;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-weight: 500 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* ───────────────── INFO / WARNING / SUCCESS / ERROR ───────────────── */
.stAlert {
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(12px);
    padding: 1rem 1.2rem !important;
}

div[data-baseweb="notification"] {
    border-radius: 12px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(30, 30, 60, 0.3);
    padding: 6px;
    border-radius: 14px;
    border: 1px solid rgba(99, 102, 241, 0.15);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 0.5rem 1.2rem;
    font-weight: 600;
    color: #cbd5e1;
    background: transparent;
    border: none;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.85) 0%, rgba(139, 92, 246, 0.85) 100%) !important;
    color: white !important;
}

/* Expander */
[data-testid="stExpander"] {
    border-radius: 14px !important;
    border: 1px solid rgba(99, 102, 241, 0.15) !important;
    background: rgba(30, 30, 60, 0.35) !important;
    overflow: hidden;
}

[data-testid="stExpander"] summary {
    color: #f1f5f9 !important;
    font-weight: 600 !important;
}

/* Code blocks */
code {
    background: rgba(30, 30, 60, 0.7) !important;
    color: #a5b4fc !important;
    border-radius: 6px;
    padding: 2px 8px;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85em;
}

/* Caption */
.stCaption, [data-testid="stCaptionContainer"] {
    color: #94a3b8 !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: rgba(15, 15, 35, 0.5); }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #6366f1, #8b5cf6); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: linear-gradient(180deg, #818cf8, #a78bfa); }

/* Hide anchor link icons in headers */
h1 a, h2 a, h3 a, h4 a { display: none !important; }

/* ───────────────── CUSTOM COMPONENT CLASSES ───────────────── */
.glass-card {
    background: rgba(30, 30, 60, 0.45);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 18px;
    padding: 1.5rem;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    margin-bottom: 1rem;
    box-shadow: 0 8px 32px -10px rgba(0, 0, 0, 0.3);
}

.glass-card:hover {
    transform: translateY(-4px);
    border-color: rgba(168, 85, 247, 0.5);
    box-shadow: 0 18px 40px -12px rgba(99, 102, 241, 0.3);
}

.feature-icon {
    font-size: 2.4rem;
    display: block;
    margin-bottom: 0.6rem;
    filter: drop-shadow(0 0 8px rgba(168, 85, 247, 0.5));
}

.feature-title {
    color: #f1f5f9;
    font-size: 1.15rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
}

.feature-desc {
    color: #94a3b8;
    font-size: 0.9rem;
    line-height: 1.55;
}

.hero-badge {
    display: inline-block;
    padding: 6px 14px;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.25), rgba(168, 85, 247, 0.25));
    border: 1px solid rgba(168, 85, 247, 0.4);
    border-radius: 100px;
    font-size: 0.78rem;
    font-weight: 600;
    color: #c4b5fd;
    letter-spacing: 0.04em;
    margin-bottom: 1rem;
    text-transform: uppercase;
}

.hero-subtitle {
    color: #94a3b8;
    font-size: 1.15rem;
    line-height: 1.6;
    max-width: 720px;
    margin-top: 0.8rem;
    font-weight: 400;
}

.gradient-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(168, 85, 247, 0.5), rgba(99, 102, 241, 0.5), transparent);
    border: none;
    margin: 2rem 0;
}

.content-box {
    background: rgba(30, 30, 60, 0.5);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
    line-height: 1.7;
    color: #e2e8f0;
}

.content-box.original {
    border-left: 4px solid #94a3b8;
}

.content-box.ai {
    border-left: 4px solid #a78bfa;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.08), rgba(168, 85, 247, 0.08));
}

.pipeline-step {
    background: rgba(30, 30, 60, 0.45);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 14px;
    padding: 1rem;
    text-align: center;
    transition: all 0.3s ease;
    height: 100%;
}

.pipeline-step:hover {
    border-color: rgba(168, 85, 247, 0.5);
    transform: scale(1.03);
}

.pipeline-step .step-num {
    display: inline-block;
    width: 32px;
    height: 32px;
    line-height: 32px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #a78bfa);
    color: white;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.pipeline-step .step-title {
    color: #f1f5f9;
    font-weight: 600;
    font-size: 0.95rem;
    margin: 0.3rem 0;
}

.pipeline-step .step-desc {
    color: #94a3b8;
    font-size: 0.78rem;
    line-height: 1.4;
}

.status-pill {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-right: 6px;
}

.status-pill.success {
    background: rgba(16, 185, 129, 0.15);
    color: #6ee7b7;
    border: 1px solid rgba(16, 185, 129, 0.4);
}

.status-pill.warning {
    background: rgba(245, 158, 11, 0.15);
    color: #fcd34d;
    border: 1px solid rgba(245, 158, 11, 0.4);
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-6px); }
}

.floating { animation: float 3s ease-in-out infinite; }

/* ───────────────── CHAT BUBBLES ───────────────── */
.chat-row {
    display: flex;
    margin-bottom: 1.2rem;
    gap: 0.8rem;
    align-items: flex-start;
}

.chat-row.user {
    flex-direction: row-reverse;
}

.chat-avatar {
    width: 38px;
    height: 38px;
    flex-shrink: 0;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    font-weight: 700;
    color: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.chat-avatar.user {
    background: linear-gradient(135deg, #6366f1, #ec4899);
}

.chat-avatar.assistant {
    background: linear-gradient(135deg, #22d3ee, #a78bfa);
}

.chat-bubble {
    max-width: 78%;
    padding: 0.9rem 1.2rem;
    border-radius: 18px;
    line-height: 1.6;
    backdrop-filter: blur(12px);
    word-wrap: break-word;
}

.chat-bubble.user {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.5), rgba(168, 85, 247, 0.5));
    color: #f1f5f9;
    border: 1px solid rgba(168, 85, 247, 0.4);
    border-top-right-radius: 4px;
}

.chat-bubble.assistant {
    background: rgba(30, 30, 60, 0.6);
    color: #e2e8f0;
    border: 1px solid rgba(34, 211, 238, 0.3);
    border-top-left-radius: 4px;
}

.chat-bubble.assistant strong { color: #c4b5fd; }
.chat-bubble.assistant code  {
    background: rgba(15, 15, 35, 0.8) !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
}

/* Error box */
.error-box {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.12), rgba(220, 38, 38, 0.08));
    border: 1px solid rgba(239, 68, 68, 0.4);
    border-left: 4px solid #ef4444;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: #fca5a5;
    margin: 1rem 0;
    font-size: 0.92rem;
    line-height: 1.55;
}

.error-box strong { color: #fecaca; }
</style>
"""


def inject_css():
    """Inject the global custom CSS into the current Streamlit page."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def page_header(icon: str, title: str, subtitle: str = "", badge: str = ""):
    """Render a consistent page header with badge, gradient title, and subtitle."""
    badge_html = f'<div class="hero-badge">{badge}</div>' if badge else ""
    subtitle_html = f'<p class="hero-subtitle">{subtitle}</p>' if subtitle else ""
    st.markdown(
        f"""
        <div style="margin-bottom: 1.5rem;">
            {badge_html}
            <h1 style="margin-top: 0;">{icon} {title}</h1>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def gradient_divider():
    """Render a thin gradient horizontal rule."""
    st.markdown('<hr class="gradient-divider"/>', unsafe_allow_html=True)


def glass_card(content_html: str):
    """Wrap arbitrary HTML in a glass card."""
    st.markdown(f'<div class="glass-card">{content_html}</div>', unsafe_allow_html=True)


def show_ai_error(error_text: str):
    """
    Display an AI error in a clearly-visible red error box.
    Use this when an AI call fails so the user sees the actual reason.
    """
    if not error_text:
        return
    # Strip the leading warning emoji if present
    msg = error_text.lstrip("⚠️ ").strip()
    st.markdown(
        f'<div class="error-box"><strong>⚠️ AI request failed</strong><br>{msg}</div>',
        unsafe_allow_html=True,
    )


def chat_bubble(role: str, content: str):
    """Render a single chat message as a styled bubble."""
    is_user = role == "user"
    # Escape HTML to prevent XSS but allow markdown rendering
    avatar_class = "user" if is_user else "assistant"
    bubble_class = "user" if is_user else "assistant"
    avatar_letter = "🧑" if is_user else "✨"
    row_class = "chat-row user" if is_user else "chat-row"

    # Use a container so Streamlit's markdown renderer handles the content
    st.markdown(
        f"""<div class="{row_class}">
            <div class="chat-avatar {avatar_class}">{avatar_letter}</div>
            <div class="chat-bubble {bubble_class}">{content}</div>
        </div>""",
        unsafe_allow_html=True,
    )
