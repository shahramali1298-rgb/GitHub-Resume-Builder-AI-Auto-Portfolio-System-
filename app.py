import streamlit as st
import requests
from collections import Counter
from fpdf import FPDF

# -------------------------------
# PAGE CONFIG (PRO UI)
# -------------------------------
st.set_page_config(
    page_title="GitHub AI Resume Builder",
    page_icon="🚀",
    layout="wide"
)

# -------------------------------
# CSS (PROFESSIONAL UI)
# -------------------------------
st.markdown("""
<style>
.main {
    background-color: #0f172a;
    color: white;
}
.title {
    font-size: 40px;
    font-weight: bold;
    color: #38bdf8;
}
.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 10px;
}
.small {
    color: #94a3b8;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🚀 GitHub AI Resume Builder</div>", unsafe_allow_html=True)

# -------------------------------
# REAL GITHUB FETCH (FIXED)
# -------------------------------
def get_github_data(username):

    user_url = f"https://api.github.com/users/{username}"
    repo_url = f"https://api.github.com/users/{username}/repos"

    user = requests.get(user_url)
    repos = requests.get(repo_url)

    # REAL FIX: status check
    if user.status_code != 200:
        return None, None

    return user.json(), repos.json()

# -------------------------------
# SKILL EXTRACTION
# -------------------------------
def extract_skills(repos):
    langs = []
    for r in repos:
        if r["language"]:
            langs.append(r["language"])
    return list(set(langs))

# -------------------------------
# REAL AI (HUGGINGFACE FREE INFERENCE)
# -------------------------------
def generate_ai_summary(name, bio, skills):

    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"

    headers = {}

    prompt = f"""
    Write a professional software developer resume summary:

    Name: {name}
    Bio: {bio}
    Skills: {', '.join(skills)}

    Make it short and impressive.
    """

    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        output = response.json()

        if isinstance(output, list):
            return output[0]["generated_text"]
        else:
            return "AI summary not available, fallback used."

    except:
        return f"{name} is a skilled developer experienced in {', '.join(skills)}."

# -------------------------------
# PDF GENERATOR
# -------------------------------
def create_pdf(name, bio, summary, skills):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="GitHub AI Resume", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Bio: {bio}", ln=True)
    pdf.ln(5)

    pdf.multi_cell(0, 10, txt=f"AI Summary:\n{summary}")
    pdf.ln(5)

    pdf.multi_cell(0, 10, txt=f"Skills:\n{', '.join(skills)}")

    file = "resume.pdf"
    pdf.output(file)
    return file

# -------------------------------
# INPUT UI
# -------------------------------
username = st.text_input("Enter GitHub Username")

if st.button("Generate Resume"):

    if not username.strip():
        st.warning("Please enter username")
        st.stop()

    user, repos = get_github_data(username.strip())

    # FIXED ERROR HANDLING
    if user is None:
        st.error("❌ GitHub user not found. Check spelling.")
        st.stop()

    name = user.get("name") or username
    bio = user.get("bio") or "No bio available"

    skills = extract_skills(repos)

    # ---------------------------
    # UI CARDS
    # ---------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("👤 Profile")
        st.write("Name:", name)
        st.write("Bio:", bio)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🧠 Skills")
        st.write(", ".join(skills))
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------
    # REPOS
    # ---------------------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Top Repositories")

    for r in repos[:5]:
        st.write(f"🔹 {r['name']} ⭐ {r['stargazers_count']}")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------
    # AI SUMMARY
    # ---------------------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🤖 AI Generated Summary")

    summary = generate_ai_summary(name, bio, skills)
    st.success(summary)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------
    # PDF DOWNLOAD
    # ---------------------------
    pdf_file = create_pdf(name, bio, summary, skills)

    with open(pdf_file, "rb") as f:
        st.download_button("📥 Download Resume PDF", f, file_name="resume.pdf")
