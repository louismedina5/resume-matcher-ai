import streamlit as st
import openai
import os
import PyPDF2

openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Resume Matcher AI", layout="centered")
st.title("📄 Resume Matcher AI")
st.write("Upload your **resume** and a **job description**, and get a match score with feedback!")

resume_file = st.file_uploader("Upload your resume (.txt or .pdf)", type=["txt", "pdf"])
job_file = st.file_uploader("Upload job description (.txt or .pdf)", type=["txt", "pdf"])

def read_file(file):
    if file is not None:
        if file.type == "application/pdf":
            reader = PyPDF2.PdfReader(file)
            return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        else:
            return file.read().decode("utf-8")
    return ""

if st.button("🔍 Analyze Match") and resume_file and job_file:
    resume_text = read_file(resume_file)
    job_text = read_file(job_file)

    with st.spinner("Analyzing..."):
        prompt = f"""
Compare the following resume and job description.
Give a match score out of 100.
Explain which skills or experiences match and which are missing.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_text}
"""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        answer = response.choices[0].message.content
        st.markdown("### ✅ Match Analysis")
        st.write(answer)
