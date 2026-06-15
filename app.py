import streamlit as st
import requests
from collections import Counter
from fpdf import FPDF

# ---------------- UI ----------------
st.set_page_config(page_title="AI Resume Builder", layout="wide")

st.markdown("""
<style>
body {background-color:#0f172a;}
.title {font-size:40px;color:#38bdf8;font-weight:bold;}
.card {background:#1e293b;padding:20px;border-radius:15px;margin:10px 0;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🚀 AI GitHub Resume Builder PRO</div>", unsafe_allow_html=True)

# ---------------- GitHub Fetch ----------------
def fetch_github(username):
    url = f"https://api.github.com/users/{username}"
    repo_url = f"https://api.github.com/users/{username}/repos"

    user = requests.get(url)
    repos = requests.get(repo_url)

    if user.status_code != 200:
        return None, None

    return user.json(), repos.json()

# ---------------- Skill Extract ----------------
def get_skills(repos):
    skills = []
    for r in repos:
        if r.get("language"):
            skills.append(r["language"])
    return list(set(skills))

# ---------------- AI FALLBACK (NO ERROR EVER) ----------------
def smart_ai_profile(name):
    return {
        "name": name,
        "bio": "Passionate Software Developer and Problem Solver.",
        "skills": ["Python", "JavaScript", "AI", "Web Development"],
        "repos": [
            {"name": "AI Chat App", "stars": 12},
            {"name": "Portfolio Website", "stars": 8},
            {"name": "Data Analysis Tool", "stars": 15},
        ]
    }

# ---------------- AI Summary ----------------
def generate_summary(name, skills):
    return f"{name} is a skilled developer experienced in {', '.join(skills)}. Focused on building scalable and modern applications."

# ---------------- PDF ----------------
def create_pdf(name, bio, summary, skills):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "AI Resume", ln=True, align="C")
    pdf.ln(10)

    pdf.cell(200, 10, f"Name: {name}", ln=True)
    pdf.cell(200, 10, f"Bio: {bio}", ln=True)
    pdf.ln(5)

    pdf.multi_cell(0, 10, f"Summary:\n{summary}")
    pdf.ln(5)

    pdf.multi_cell(0, 10, f"Skills:\n{', '.join(skills)}")

    file = "resume.pdf"
    pdf.output(file)
    return file

# ---------------- INPUT ----------------
query = st.text_input("Enter GitHub Username OR Your Name")

if st.button("Generate Resume"):

    # TRY GITHUB FIRST
    user, repos = fetch_github(query.strip())

    if user:
        name = user.get("name") or query
        bio = user.get("bio") or "No bio available"
        skills = get_skills(repos)
        repos_list = repos

        mode = "GitHub Profile Loaded"

    else:
        # FALLBACK AI MODE (NO ERROR EVER)
        data = smart_ai_profile(query)

        name = data["name"]
        bio = data["bio"]
        skills = data["skills"]

        repos_list = data["repos"]

        mode = "AI Generated Profile (No GitHub Found)"

    # ---------------- DASHBOARD ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("👤 Profile")
        st.write(name)
        st.write(bio)
        st.info(mode)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🧠 Skills")
        st.write(", ".join(skills))
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- REPOS ----------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Projects")

    for r in repos_list[:5]:
        st.write(f"🔹 {r['name']} ⭐ {r['stars'] if 'stars' in r else r.get('stargazers_count', 0)}")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- SUMMARY ----------------
    summary = generate_summary(name, skills)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🤖 AI Summary")
    st.success(summary)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- PDF ----------------
    pdf_file = create_pdf(name, bio, summary, skills)

    with open(pdf_file, "rb") as f:
        st.download_button("📥 Download Resume", f, file_name="resume.pdf")
