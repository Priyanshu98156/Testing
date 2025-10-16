import streamlit as st
import fitz
import docx
from io import BytesIO
import ollama
import json
import re

def ats_checker():
        
    st.header("📊 ATS Checker")
    st.write("Upload your resume and paste the job description below:")

    resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    job_desc = st.text_area("Paste Job Description")

    def extract_text_from_pdf(file):
        text = ""
        file.seek(0)
        with fitz.open(stream=file.read(), filetype="pdf") as pdf:
            for page in pdf:
                text += page.get_text("text")
        return text.strip()

    def extract_text_from_docx(file):
        file.seek(0)
        doc = docx.Document(BytesIO(file.read()))
        return "\n".join([para.text for para in doc.paragraphs]).strip()

    def extract_resume_text(file):
        ext = file.name.split(".")[-1].lower()
        if ext == "pdf":
            return extract_text_from_pdf(file)
        elif ext == "docx":
            return extract_text_from_docx(file)
        else:
            st.error("Unsupported file format. Please upload PDF or DOCX.")
            return ""

    def clean_text(x):
        x = re.sub(r'\s+', ' ', x)
        x = re.sub(r'http\S+', '', x)
        x = re.sub(r'[^A-Za-z0-9 .,]', '', x)
        return x.strip()

    def extract_json(text):
        text = text.strip()
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"```$", "", text)
        match = re.search(r"\{.*\}", text, re.DOTALL)
        return match.group(0) if match else "{}"

    if st.button("Check ATS Score"):
        if resume_file and job_desc.strip():
            with st.spinner("Analyzing..."):
                resume_text = extract_resume_text(resume_file)
                resume_text = clean_text(resume_text)
                job_desc_clean = clean_text(job_desc)

                if not resume_text:
                    st.error("⚠️ Could not extract text from the uploaded file.")
                else:
                    prompt_content = f"""
                    You are an expert resume analyst. Your task is to analyze a candidate's resume and a job description to determine their fit.
                    Respond ONLY with a JSON object like:
                    {{"match_score": 85}}

                    [JOB DESCRIPTION]
                    {job_desc_clean}

                    [CANDIDATE RESUME]
                    {resume_text}
                    """

                    response = ollama.chat(
                        model='gemma3',
                        messages=[{'role': 'user', 'content': prompt_content}]
                    )

                    try:
                        raw_content = response.get('message', {}).get('content', '') or response.get('content', '')
                        json_str = extract_json(raw_content)
                        ats_score_data = json.loads(json_str)
                        score = ats_score_data.get('match_score', 'N/A')

                        if isinstance(score, str) and score.isdigit():
                            score = int(score)

                        st.success(f"✅ ATS Score: {score}%")

                    except Exception as e:
                        st.error(f"⚠️ Failed to parse model response: {e}")
                        st.write("Raw response:", response)

        else:
            st.warning("Please upload a resume and paste the job description!")
