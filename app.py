import streamlit as st
from transformers import pipeline
import random

st.set_page_config(page_title="AI GitHub Resume Builder", layout="centered")

st.title("🚀 AI GitHub Resume Builder (Clean Version)")
st.write("Generate structured developer profile from any name")

# ----------------------------
# Model
# ----------------------------
@st.cache_resource
def load_model():
    try:
        return pipeline("text-generation", model="distilgpt2")
    except:
        return None

model = load_model()

# ----------------------------
# Safe structured fallback
# ----------------------------
def safe_resume(name):
    skills = [
        "Python", "Machine Learning", "Data Science",
        "Web Development", "GitHub Projects", "APIs"
    ]

    projects = [
        "AI Resume Generator",
        "GitHub Profile Analyzer",
        "Portfolio Website Builder",
        "Chatbot Application",
        "Automation Scripts Toolkit"
    ]

    return f"""
====================================
👤 GITHUB DEVELOPER PROFILE
====================================

Name: {name}

📌 ABOUT
{name} is a software developer focused on AI, web development, and scalable applications.

🧠 SKILLS
- {', '.join(random.sample(skills, 4))}

📂 PROJECTS
1. {random.choice(projects)}
2. {random.choice(projects)}
3. {random.choice(projects)}

🚀 GITHUB SUMMARY
Active developer building real-world AI and automation projects.

🔗 PROFILE LINK
https://github.com/{name.lower().replace(" ", "-")}
====================================
"""

# ----------------------------
# AI generator (controlled)
# ----------------------------
def generate(name):
    if model:
        try:
            prompt = f"""
Write ONLY a structured GitHub developer profile.

Name: {name}

Format:
- About
- Skills
- Projects
- GitHub Summary

Do not add extra text.
"""
            out = model(prompt, max_length=180, num_return_sequences=1)[0]["generated_text"]

            # Safety filter (remove garbage)
            if "API" in out or "hash" in out or "Shahram-ali is" in out:
                return safe_resume(name)

            return out

        except:
            return safe_resume(name)
    else:
        return safe_resume(name)

# ----------------------------
# UI
# ----------------------------
name = st.text_input("Enter Your Name")

if st.button("Generate Resume"):
    if name.strip() == "":
        st.warning("Please enter a valid name")
    else:
        result = generate(name)

        st.subheader("📄 Generated Profile")
        st.text_area("Output", result, height=450)
