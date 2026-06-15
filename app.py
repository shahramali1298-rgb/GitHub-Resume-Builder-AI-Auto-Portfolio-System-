import streamlit as st
import requests
import pandas as pd
from collections import Counter
from fpdf import FPDF
from transformers import pipeline

# -------------------------------
# HuggingFace Model (FREE)
# -------------------------------
@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="google/flan-t5-small")

model = load_model()

# -------------------------------
# GitHub Data Fetch Function
# -------------------------------
def get_github_data(username):
    url = f"https://api.github.com/users/{username}"
    repos_url = f"https://api.github.com/users/{username}/repos"

    user_data = requests.get(url).json()
    repos_data = requests.get(repos_url).json()

    return user_data, repos_data

# -------------------------------
# Skill Extraction
# -------------------------------
def extract_skills(repos):
    languages = []

    for repo in repos:
        if repo["language"]:
            languages.append(repo["language"])

    skill_count = Counter(languages)
    return skill_count

# -------------------------------
# AI Summary Generator
# -------------------------------
def generate_summary(name, bio, skills):
    input_text = f"""
    Create a professional resume summary for a software developer.

    Name: {name}
    Bio: {bio}
    Skills: {', '.join(skills)}

    Make it short and professional.
    """

    result = model(input_text, max_length=100)
    return result[0]['generated_text']

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

    pdf.multi_cell(0, 10, txt=f"AI Summary:\n{summary}")
    pdf.ln(5)

    pdf.multi_cell(0, 10, txt=f"Skills:\n{', '.join(skills)}")

    file_name = "resume.pdf"
    pdf.output(file_name)

    return file_name

# -------------------------------
# STREAMLIT UI
# -------------------------------
st.set_page_config(page_title="GitHub AI Resume Builder", layout="wide")

st.title("🚀 GitHub AI Resume Builder")
st.write("Generate AI-powered resume from your GitHub profile")

username = st.text_input("Enter GitHub Username")

if st.button("Generate Resume"):

    if username:
        user_data, repos = get_github_data(username)

        if "message" in user_data:
            st.error("User not found!")
        else:
            name = user_data.get("name") or username
            bio = user_data.get("bio") or "No bio available"

            skills_dict = extract_skills(repos)
            skills = list(skills_dict.keys())

            st.subheader("👤 Profile")
            st.write("Name:", name)
            st.write("Bio:", bio)

            st.subheader("🧠 Skills Detected")
            st.write(skills)

            st.subheader("📊 Top Repositories")

            for repo in repos[:5]:
                st.write(f"🔹 {repo['name']} - ⭐ {repo['stargazers_count']}")

            # AI Summary
            summary = generate_summary(name, bio, skills)

            st.subheader("🤖 AI Generated Summary")
            st.success(summary)

            # PDF
            pdf_file = create_pdf(name, bio, summary, skills)

            with open(pdf_file, "rb") as f:
                st.download_button("📥 Download Resume PDF", f, file_name=pdf_file)

    else:
        st.warning("Please enter username")
