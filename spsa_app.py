import streamlit as st
import google.generativeai as genai
import json

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SPSA · Smart Personal Study Assistant",
    page_icon="📖",
    layout="centered",
)

# ── Custom CSS: light-pink palette + typewriter font ─────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Courier+Prime:ital,wght@0,400;0,700;1,400&family=Special+Elite&display=swap');

:root {
    --pink-50:  #fff0f3;
    --pink-100: #ffe0e8;
    --pink-200: #ffb3c6;
    --pink-300: #ff85a1;
    --pink-400: #ff4d79;
    --pink-dark: #c9184a;
    --ink:       #2d1b23;
    --ink-light: #6b3a4a;
    --white:     #fffbfc;
    --shadow:    rgba(201,24,74,0.12);
}

html, body, [class*="css"] {
    font-family: 'Courier Prime', 'Courier New', monospace !important;
    background-color: var(--pink-50) !important;
    color: var(--ink) !important;
}

.main .block-container {
    max-width: 780px;
    padding: 2.5rem 2rem 4rem;
    background: var(--white);
    border: 2px solid var(--pink-200);
    border-radius: 4px;
    box-shadow: 6px 6px 0px var(--pink-200), 12px 12px 0px var(--pink-100);
    margin-top: 2rem;
}

.spsa-header {
    text-align: center;
    margin-bottom: 2rem;
    border-bottom: 3px double var(--pink-300);
    padding-bottom: 1.2rem;
}
.spsa-header h1 {
    font-family: 'Special Elite', serif !important;
    font-size: 2.4rem !important;
    color: var(--pink-dark) !important;
    letter-spacing: 0.04em;
    margin: 0 0 0.3rem;
}
.spsa-header p {
    color: var(--ink-light) !important;
    font-size: 0.95rem;
    font-style: italic;
    margin: 0;
}

.section-label {
    font-family: 'Special Elite', serif !important;
    font-size: 0.78rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--pink-dark);
    margin-bottom: 0.4rem;
    display: block;
}

textarea, .stTextArea textarea {
    font-family: 'Courier Prime', monospace !important;
    background: var(--pink-50) !important;
    border: 1.5px solid var(--pink-200) !important;
    border-radius: 3px !important;
    color: var(--ink) !important;
    font-size: 0.93rem !important;
    padding: 0.8rem !important;
    resize: vertical;
}
textarea:focus, .stTextArea textarea:focus {
    border-color: var(--pink-300) !important;
    box-shadow: 0 0 0 3px var(--shadow) !important;
}

.stSelectbox > div > div, .stNumberInput > div > div > input {
    font-family: 'Courier Prime', monospace !important;
    background: var(--pink-50) !important;
    border: 1.5px solid var(--pink-200) !important;
    border-radius: 3px !important;
    color: var(--ink) !important;
}

.stButton > button {
    font-family: 'Special Elite', serif !important;
    background: var(--pink-dark) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 3px !important;
    padding: 0.7rem 2.2rem !important;
    font-size: 1rem !important;
    letter-spacing: 0.08em !important;
    cursor: pointer !important;
    box-shadow: 3px 3px 0 var(--pink-300) !important;
    transition: transform 0.1s, box-shadow 0.1s !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translate(-1px,-1px) !important;
    box-shadow: 4px 4px 0 var(--pink-300) !important;
    background: #a01038 !important;
}
.stButton > button:active {
    transform: translate(2px,2px) !important;
    box-shadow: 1px 1px 0 var(--pink-300) !important;
}

.result-card {
    background: var(--pink-50);
    border: 1.5px solid var(--pink-200);
    border-left: 4px solid var(--pink-dark);
    border-radius: 3px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1.2rem;
    font-size: 0.94rem;
    line-height: 1.7;
}
.result-card h3 {
    font-family: 'Special Elite', serif !important;
    color: var(--pink-dark) !important;
    font-size: 1rem !important;
    margin: 0 0 0.6rem;
    letter-spacing: 0.05em;
}

hr {
    border: none;
    border-top: 2px dashed var(--pink-200);
    margin: 1.5rem 0;
}

section[data-testid="stSidebar"] {
    background: var(--pink-100) !important;
    border-right: 2px solid var(--pink-200) !important;
}
section[data-testid="stSidebar"] * {
    font-family: 'Courier Prime', monospace !important;
    color: var(--ink) !important;
}

.stAlert {
    font-family: 'Courier Prime', monospace !important;
    border-radius: 3px !important;
}

.spsa-footer {
    text-align: center;
    font-size: 0.75rem;
    color: var(--ink-light);
    font-style: italic;
    margin-top: 2.5rem;
    padding-top: 1rem;
    border-top: 1px solid var(--pink-100);
}
</style>
""",
    unsafe_allow_html=True,
)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="spsa-header">
    <h1>📖 S P S A</h1>
    <p>Smart Personal Study Assistant · by Ayra Omar</p>
</div>
""",
    unsafe_allow_html=True,
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")

    gemini_api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="AIza...",
        help="Get your free key at aistudio.google.com",
    )

    st.markdown(
        "<small>🔑 Get a free key at <a href='https://aistudio.google.com' target='_blank'>aistudio.google.com</a></small>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    subject_domain = st.selectbox(
        "Subject Domain",
        [
            "General",
            "Artificial Intelligence",
            "Data Structures & Algorithms",
            "Mathematics",
            "Physics",
            "Computer Networks",
            "Operating Systems",
            "Software Engineering",
            "Database Systems",
        ],
        index=1,
    )

    academic_level = st.selectbox(
        "Academic Level",
        [
            "Undergraduate (Year 1–2)",
            "Undergraduate (Year 3–4)",
            "Graduate / Masters",
            "High School",
        ],
        index=0,
    )

    num_questions = st.number_input(
        "Practice Questions to Generate",
        min_value=1,
        max_value=5,
        value=1,
        step=1,
    )

    num_keypoints = st.number_input(
        "Key Points in Summary",
        min_value=2,
        max_value=7,
        value=3,
        step=1,
    )

    st.markdown("---")
    st.markdown(
        """
    <small>
    <b>Roll No:</b> 24L-0628<br>
    <b>Course:</b> AI Lab<br>
    <b>Instructor:</b> Mr. Riaz Ahmed
    </small>
    """,
        unsafe_allow_html=True,
    )


# ── Helper: call Gemini ───────────────────────────────────────────────────────
def call_gemini(
    api_key: str, text: str, subject: str, level: str, num_kp: int, num_q: int
) -> dict:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-pro")

    prompt = f"""You are an expert academic tutor specialising in {subject}
for {level} students. Respond with valid JSON only — no markdown fences, no preamble, nothing else.
Use exactly this structure:
{{
  "key_points": ["point 1", "point 2", ...],
  "practice_questions": ["Q1?", "Q2?", ...]
}}
Produce exactly {num_kp} key points and {num_q} practice question(s).
Tailor depth and language to a {level} student.

Here is the study material:

{text}"""

    response = model.generate_content(prompt)
    raw = response.text.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
    return json.loads(raw)


# ── Main input ────────────────────────────────────────────────────────────────
st.markdown(
    '<span class="section-label">Paste your study material below</span>',
    unsafe_allow_html=True,
)

user_text = st.text_area(
    label="",
    placeholder="Paste lecture notes, textbook paragraphs, or any academic text here...",
    height=240,
    label_visibility="collapsed",
)

st.markdown("")
study_btn = st.button("✦ Generate Study Materials")

# ── Processing ────────────────────────────────────────────────────────────────
if study_btn:
    if not gemini_api_key:
        st.error("⚠  Please enter your Gemini API key in the sidebar.")
    elif not user_text.strip():
        st.warning("⚠  Please paste some study material first.")
    else:
        with st.spinner("Thinking through your material..."):
            try:
                result = call_gemini(
                    api_key=gemini_api_key,
                    text=user_text,
                    subject=subject_domain,
                    level=academic_level,
                    num_kp=num_keypoints,
                    num_q=num_questions,
                )

                st.markdown("<hr>", unsafe_allow_html=True)

                # Key Points
                st.markdown(
                    '<span class="section-label">📌 Key Takeaways</span>',
                    unsafe_allow_html=True,
                )
                kp_html = "<div class='result-card'><h3>Summary</h3><ul>"
                for pt in result.get("key_points", []):
                    kp_html += f"<li>{pt}</li>"
                kp_html += "</ul></div>"
                st.markdown(kp_html, unsafe_allow_html=True)

                # Practice Questions
                st.markdown(
                    '<span class="section-label">🧠 Practice Questions</span>',
                    unsafe_allow_html=True,
                )
                for i, q in enumerate(result.get("practice_questions", []), 1):
                    st.markdown(
                        f"<div class='result-card'><h3>Question {i}</h3><p>{q}</p></div>",
                        unsafe_allow_html=True,
                    )

            except Exception as e:
                err = str(e).lower()
                if "api_key" in err or "api key" in err or "invalid" in err:
                    st.error("❌ Invalid API key. Double-check the key in the sidebar.")
                elif "quota" in err or "limit" in err:
                    st.error("❌ API quota exceeded. Wait a moment and try again.")
                elif "json" in err:
                    st.error(
                        "❌ Couldn't parse the AI response. Try again or simplify your input."
                    )
                else:
                    st.error(f"❌ Error: {e}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="spsa-footer">
    SPSA · AI Lab Project · FAST-NUCES · 2026
</div>
""",
    unsafe_allow_html=True,
)
print([m.name for m in genai.list_models()])
