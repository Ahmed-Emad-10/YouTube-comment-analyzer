from pathlib import Path

import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="YT Comment Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Outfit', sans-serif !important;
    background-color: #f5f4f0 !important;
    color: #1a1a1a !important;
}
#MainMenu, footer, header { visibility: hidden; }

.block-container {
    max-width: 780px !important;
    padding: 4rem 2rem 3rem 2rem !important;
}

.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #e05a2b;
    margin-bottom: 1rem;
}
.hero-title {
    font-size: 3.6rem;
    font-weight: 800;
    color: #1a1a1a;
    line-height: 1.05;
    margin-bottom: 1rem;
    letter-spacing: -0.03em;
}
.hero-title span { color: #e05a2b; }
.hero-desc {
    font-size: 1.05rem;
    font-weight: 300;
    color: #666;
    line-height: 1.7;
    margin-bottom: 2.8rem;
    max-width: 520px;
}

.stTextInput > div > div > input {
    background-color: #ffffff !important;
    border: 1.5px solid #ddd !important;
    border-radius: 10px !important;
    color: #1a1a1a !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.88rem !important;
    padding: 0.9rem 1.1rem !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: #e05a2b !important;
    box-shadow: 0 0 0 3px rgba(224,90,43,0.10) !important;
}
.stTextInput label { display: none !important; }

.stButton > button {
    background-color: #e05a2b !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.7rem 2rem !important;
    transition: background-color 0.2s, transform 0.15s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background-color: #c44d22 !important;
    transform: translateY(-1px) !important;
}

.divider { height: 1px; background: #e0ddd8; margin: 2.5rem 0; }

.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 1.2rem;
}

.step-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.6rem 0;
    font-size: 0.9rem;
    color: #444;
}
.step-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #e05a2b;
    flex-shrink: 0;
    animation: pulse 1.2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.7); }
}

.result-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #1a1a1a;
    letter-spacing: -0.03em;
    margin-bottom: 0.3rem;
}
.result-url {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #999;
    margin-bottom: 2rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

div[data-testid="stTabs"] { border-bottom: 1px solid #e0ddd8; margin-bottom: 1.5rem; }
div[data-testid="stTabs"] button {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    color: #999 !important;
    padding: 0.6rem 1rem !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #1a1a1a !important;
    border-bottom: 2px solid #e05a2b !important;
    font-weight: 600 !important;
}

.report-wrap {
    background: #fff;
    border: 1px solid #e0ddd8;
    border-radius: 12px;
    padding: 2.2rem 2.4rem;
    line-height: 1.85;
    font-size: 0.95rem;
    color: #2a2a2a;
}

.stDownloadButton > button {
    background-color: transparent !important;
    color: #e05a2b !important;
    border: 1.5px solid #e05a2b !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    margin-top: 1rem !important;
    width: 100% !important;
}
.stDownloadButton > button:hover {
    background-color: #e05a2b !important;
    color: #fff !important;
}

.back-btn button {
    background-color: transparent !important;
    color: #999 !important;
    border: 1px solid #ddd !important;
    font-size: 0.85rem !important;
    padding: 0.4rem 1.2rem !important;
    width: auto !important;
    margin-bottom: 1.5rem !important;
}
.back-btn button:hover {
    color: #1a1a1a !important;
    border-color: #999 !important;
    transform: none !important;
    background-color: transparent !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
for key, default in {
    "page": "input",
    "report": None,
    "video_url": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — INPUT
# ══════════════════════════════════════════════════════════════════════════════
def page_input():
    st.markdown('<div class="hero-eyebrow">YouTube Comment Intelligence</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-title">Understand your<br>audience <span>deeply.</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="hero-desc">Paste any YouTube URL. We scrape the comments, '
        'run sentiment & topic analysis, then let AI extract what people love '
        'and what frustrates them.</div>',
        unsafe_allow_html=True,
    )

    with st.form("url_form"):
        url = st.text_input(
            label="url",
            placeholder="https://www.youtube.com/watch?v=...",
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("Run Analysis →")

    if submitted:
        if not url.strip():
            st.error("Please enter a valid YouTube URL.")
            return

        st.session_state.video_url = url.strip()
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Pipeline Running</div>', unsafe_allow_html=True)

        steps = [
            "Scraping comments from YouTube",
            "Running topic modeling (BERTopic)",
            "Analyzing sentiment per comment",
            "AI crews extracting insights & complaints",
            "Report writer synthesizing final report",
        ]

        step_placeholder = st.empty()

        def render_steps(active_index):
            rows = ""
            for j, s in enumerate(steps):
                if j < active_index:
                    rows += f'<div class="step-row">✓ &nbsp;{s}</div>'
                elif j == active_index:
                    rows += f'<div class="step-row"><div class="step-dot"></div>{s}</div>'
            step_placeholder.markdown(rows, unsafe_allow_html=True)

        try:
            from new_main import CommentAnalysisFlow

            render_steps(0)
            flow = CommentAnalysisFlow()
            flow.state.video_url = url.strip()

            render_steps(1)
            flow.kickoff()

            # ── Read outputs written by the Flow ──────────────────────────────
            render_steps(4)

            # Report
            report_path = Path("output/report.md")
            report_text = (
                report_path.read_text(encoding="utf-8")
                if report_path.exists()
                else "⚠️ Report file not found at output/report.md"
            )

            st.session_state.report = report_text

            step_placeholder.markdown(
                "".join([f'<div class="step-row">✓ &nbsp;{s}</div>' for s in steps]),
                unsafe_allow_html=True,
            )

            st.session_state.page = "results"
            st.rerun()

        except Exception as e:
            st.error(f"Something went wrong: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — RESULTS
# ══════════════════════════════════════════════════════════════════════════════
def page_results():
    col_back, _ = st.columns([1, 5])
    with col_back:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("← Back"):
            st.session_state.page     = "input"
            st.session_state.report   = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="result-title">Analysis Complete</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="result-url">{st.session_state.video_url}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-label">AI-generated report</div>', unsafe_allow_html=True)
    report = st.session_state.report
    if report:
        st.markdown('<div class="report-wrap">', unsafe_allow_html=True)
        st.markdown(report)
        st.markdown('</div>', unsafe_allow_html=True)

        st.download_button(
            label="⬇  Download Report (.md)",
            data=report,
            file_name="yt_analysis_report.md",
            mime="text/markdown",
        )
    else:
        st.info("No report available.")


# ── Router ────────────────────────────────────────────────────────────────────
if st.session_state.page == "input":
    page_input()
else:
    page_results()