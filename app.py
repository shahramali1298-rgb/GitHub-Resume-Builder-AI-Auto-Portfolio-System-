import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="AI GitHub Resume Builder", layout="centered")

st.title("🚀 AI GitHub Resume Builder (Pro Version)")
st.write("Generate structured developer profile using HuggingFace FLAN-T5")

# -----------------------------
# Load Model (BEST for instructions)
# -----------------------------
@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="google/flan-t5-small")

model = load_model()

# -----------------------------
# Safe Generator
# -----------------------------
def generate_profile(name):
    prompt = f"""
Create a professional GitHub developer profile.

Name: {name}

Return format:
About:
Skills:
Projects:
GitHub Summary:

Keep it short and structured.
"""

    result = model(prompt, max_length=256)[0]["generated_text"]

    return result

# -----------------------------
# UI
# -----------------------------
name = st.text_input("Enter Your Name")

if st.button("Generate Resume"):
    if name.strip() == "":
        st.warning("Please enter a valid name")
    else:
        output = generate_profile(name)

        st.subheader("📄 Generated GitHub Profile")
        st.text_area("Result", output, height=400)
