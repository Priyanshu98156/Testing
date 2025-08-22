import streamlit as st
import subprocess
import os

st.title("Resume Generator (LaTeX)")

# Inputs
name = st.text_input("Enter your name")
job_title = st.text_input("Enter your job title")
email = st.text_input("Enter your email")
phone = st.text_input("Enter your phone number")
linkedin = st.text_input("Enter your LinkedIn URL")
github = st.text_input("Enter your GitHub URL")

summary = st.text_area("Professional Summary")
skills = st.text_area("Skills (comma separated)")
experience = st.text_area("Work Experience (use \\n for new lines)")
education = st.text_area("Education (use \\n for new lines)")

if st.button("Generate Resume"):
    # LaTeX Template
    latex_code = fr"""
\documentclass[12pt]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[a4paper,margin=1in]{{geometry}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}
\hypersetup{{colorlinks=true, urlcolor=blue}}

\begin{{document}}
\begin{{center}}
    \Huge \textbf{{{name}}} \\
    \vspace{{5pt}}
    \large {job_title} \\
    \vspace{{5pt}}
    \normalsize {email} \; | \; {phone} \; | \; 
    \href{{{linkedin}}}{{LinkedIn}} \; | \; \href{{{github}}}{{GitHub}} \\
\end{{center}}

\section*{{Summary}}
{summary}

\section*{{Skills}}
\begin{{itemize}}[leftmargin=*]
    {"".join([f"\\item {skill.strip()}\n" for skill in skills.split(",") if skill.strip()])}
\end{{itemize}}

\section*{{Experience}}
\begin{{itemize}}[leftmargin=*]
    {"".join([f"\\item {line.strip()}\n" for line in experience.split("\\n") if line.strip()])}
\end{{itemize}}

\section*{{Education}}
\begin{{itemize}}[leftmargin=*]
    {"".join([f"\\item {line.strip()}\n" for line in education.split("\\n") if line.strip()])}
\end{{itemize}}

\end{{document}}
"""

    # Save .tex file
    with open("resume.tex", "w", encoding="utf-8") as f:
        f.write(latex_code)

    # Run pdflatex
    try:
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "resume.tex"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        st.success("PDF generated successfully ✅")
        with open("resume.pdf", "rb") as pdf_file:
            st.download_button("Download Resume", pdf_file, file_name="resume.pdf")
    except subprocess.CalledProcessError as e:
        st.error("LaTeX compilation failed ❌")
        st.text(e.stdout)
