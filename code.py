import streamlit as st
from transformers import pipeline
import docx2txt
import pdfplumber
import os

def extract_text_from_file(uploaded_file):
    if uploaded_file is not None:
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
        if file_extension == ".pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
            return text
        
        elif file_extension in [".docx", ".doc"]:
            text = docx2txt.process(uploaded_file)
            return text
        
    return None

# Load AI Model
generator = pipeline("text-generation", model="HuggingFaceH4/zephyr-7b-alpha")

st.title("AI Resume Analyzer & Builder")

# Upload Resume File
uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx", "doc"])
extracted_text = ""

if uploaded_file:
    extracted_text = extract_text_from_file(uploaded_file)
    if extracted_text:
        st.text_area("Extracted Resume Content", extracted_text, height=300)
    else:
        st.error("Could not extract text from the file. Please upload a valid resume.")

# Company Skill Requirements (Modify as needed)
company_required_skills = {"Python", "Machine Learning", "Data Analysis", "AI", "NLP", "Deep Learning"}

# User Inputs
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
skills = st.text_area("Skills (comma-separated)")
experience = st.text_area("Work Experience")
education = st.text_area("Education")

# Compare Skills with Company Requirements
if skills:
    user_skills = set([s.strip() for s in skills.split(",")])
    missing_skills = company_required_skills - user_skills
    if missing_skills:
        st.warning(f"You are missing the following skills required by the company: {', '.join(missing_skills)}")
    else:
        st.success("Your skills match the company's requirements!")

if st.button("Generate Resume"):
    # Create Prompt
    prompt = f"""
    Name: {name}
    Email: {email}
    Phone: {phone}
    Skills: {skills}
    Experience: {experience}
    Education: {education}
    Generate a professional resume using this information.
    """

    # Generate Resume
    resume_text = generator(prompt, max_length=500, num_return_sequences=1)[0]["generated_text"]
    
    st.subheader("Generated Resume:")
    st.text_area("Resume Output", resume_text, height=300)
