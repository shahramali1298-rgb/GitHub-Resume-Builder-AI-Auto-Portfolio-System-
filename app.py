import streamlit as st
from transformers import pipeline
import random

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="AI Resume Builder", layout="centered")

st.title("🚀 AI GitHub Resume Builder")
st.write("Enter any name and generate a complete AI portfolio (Streamlit + HuggingFace)")

# ----------------------------
# Safe AI Model Loader (No crash)
# ----------------------------
@st.cache_resource
def load_model():
    try:
        generator = pipeline("text-generation", model="distilgpt2")
        return generator
    except:
        return None

model = load_model()

# ----------------------------
# Fallback Generator (IMPORTANT)
# ----------------------------
def fallback_resume(name):
    skills_pool = [
        "Python", "Machine Learning", "Data Analysis",
        "Web Development", "GitHub Projects", "AI Integration"
    ]

    projects = [
        "AI Chatbot System",
        "GitHub Profile Analyzer",
        "Smart Resume Generator",
        "Data Science Dashboard",
        "Automation Script Toolkit"
    ]

    return f"""
👤 Name: {name}

🧠 About:
{name} is a passionate developer interested in Artificial Intelligence and modern software development.

💡 Skills:
- {', '.join(random.sample(skills_pool, 4))}

📂 Projects:
- {random.choice(projects)}
- {random.choice(projects)}
- {random.choice(projects)}

📊 GitHub Style Summary:
Active developer building AI-powered and automation-based solutions.

⭐ Strengths:
Problem Solving, Consistency, Fast Learning
"""

# ----------------------------
# AI Generator
# ----------------------------
def generate_resume(name):
    if model:
        try:
            prompt = f"Create a professional GitHub developer profile for {name} including skills and projects:"
            result = model(prompt, max_length=200, num_return_sequences=1)
            return result[0]["generated_text"]
        except:
            return fallback_resume(name)
    else:
        return fallback_resume(name)

# ----------------------------
# UI Input
# ----------------------------
name = st.text_input("Enter Your Name")

if st.button("Generate Resume"):
    if name.strip() == "":
        st.warning("Please enter a valid name")
    else:
        output = generate_resume(name)

        st.subheader("📄 Generated Resume")
        st.text_area("Result", output, height=400)
