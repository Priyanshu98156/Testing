import streamlit as st
import subprocess
import os

st.title("Resume Generator")

name = st.text_input("Enter your name")
job_title = st.text_input("Enter your job title")

if st.button("Generate Resume"):
    latex_code = fr"""
\documentclass[12pt]{{article}}
\usepackage[utf8]{{inputenc}}
\begin{{document}}
\begin{{center}}
    \Huge \textbf{{{name}}} \\
    \large {job_title} \\
\end{{center}}

\section*{{About Me}}
This is a demo LaTeX resume generated using Streamlit.

\end{{document}}
"""

    # Write .tex file
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
        st.text(e.stdout)  # show pdflatex output in Streamlit
