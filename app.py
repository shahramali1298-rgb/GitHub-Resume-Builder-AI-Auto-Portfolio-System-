import streamlit as st
import requests
from collections import Counter
from fpdf import FPDF

# -------------------------------
# GitHub Fetch
# -------------------------------
def get_github_data(username):
    user_url = f"https://api.github.com/users/{username}"
    repo_url = f"https://api.github.com/users/{username}/repos"

    user = requests.get(user_url).json()
    repos = requests.get(repo_url).json()

    return user, repos

# -------------------------------
# Skill Extraction
# -------------------------------
def extract_skills(repos):
    langs = []
    for r in repos:
        if r.get("language"):
            langs.append(r["language"])

    return list(Counter(langs).keys())

# -------------------------------
# SIMPLE AI SUMMARY (NO TRANSFORMERS)
# -------------------------------
def generate_ai_summary(name, bio, skills):
    skills_text = ", ".join(skills)

    prompt = f"""
    Developer Name: {name}
    Bio: {bio}
    Skills: {skills_text}

    Write a professional short resume summary in 3 lines.
    """

    # lightweight "AI-like" logic (works everywhere)
    summary = (
        f"{name} is a skilled software developer. "
        f"Experienced in {skills_text}. "
        f"{bio if bio else 'Passionate about building scalable applications.'}"
    )

    return summary

# -------------------------------
# PDF Generator
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

    pdf.multi_cell(0, 10, txt=f"Summary:\n{summary}")
    pdf.ln(5)

    pdf.multi_cell(0, 10, txt=f"Skills:\n{', '.join(skills)}")

    file = "resume.pdf"
    pdf.output(file)

    return file

# -------------------------------
# UI
# -------------------------------
st.set_page_config(page_title="GitHub AI Resume Builder", layout="wide")

st.title("🚀 GitHub AI Resume Builder (Fixed Version)")
st.write("Fully working on Python 3.10 + Streamlit Cloud")

username = st.text_input("Enter GitHub Username")

if st.button("Generate Resume"):

    if username:
        user, repos = get_github_data(username)

        if "message" in user:
            st.error("User not found!")
        else:
            name = user.get("name") or username
            bio = user.get("bio") or "No bio available"

            skills = extract_skills(repos)

            st.subheader("👤 Profile")
            st.write(name)
            st.write(bio)

            st.subheader("🧠 Skills")
            st.write(skills)

            st.subheader("📊 Top Repos")
            for r in repos[:5]:
                st.write(f"🔹 {r['name']} ⭐ {r['stargazers_count']}")

            summary = generate_ai_summary(name, bio, skills)

            st.subheader("🤖 AI Summary")
            st.success(summary)

            pdf_file = create_pdf(name, bio, summary, skills)

            with open(pdf_file, "rb") as f:
                st.download_button("📥 Download Resume", f, file_name="resume.pdf")

    else:
        st.warning("Enter username first")
