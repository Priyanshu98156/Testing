import streamlit as st
import subprocess
import os
from jinja2 import Environment, FileSystemLoader

# Load Jinja2 with custom delimiters
env = Environment(
    block_start_string='((*',
    block_end_string='*))',
    variable_start_string='<<',
    variable_end_string='>>',
    comment_start_string='((=',
    comment_end_string='=))',
    loader=FileSystemLoader('.')  # Looks for resume.tex in current folder
)

st.title("Resume Generator (LaTeX)")

# Inputs
name = st.text_input("Enter your name")
telephone = st.text_input("Enter your phone number")
email = st.text_input("Enter your email")
linkedin = st.text_input("Enter your LinkedIn URL")
github = st.text_input("Enter your GitHub URL")
hackerrank_id = st.text_input("Enter your Hackerrank URL")
# job_title = st.text_input("Enter your job title")
city = st.text_input("Enter your city")

if st.button("Generate Resume"):
    try:
        # Load Jinja2 template
        template = env.get_template("resume.tex")

        # Render with user input
        latex_code = template.render(
            name=name,
            telephone=telephone,
            email=email,
            linkedin=linkedin,
            github=github,
            hackerrank_id=hackerrank_id,
            # job_title=job_title,
            city=city
        )

        # Save final LaTeX file
        tex_file = "resumefinal.tex"
        with open(tex_file, "w", encoding="utf-8") as f:
            f.write(latex_code)

        # Run pdflatex
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        # Correct output file name
        pdf_file = "resumefinal.pdf"

        if os.path.exists(pdf_file):
            st.success("PDF generated successfully ✅")
            with open(pdf_file, "rb") as f:
                st.download_button("Download Resume", f, file_name="resume.pdf")
        else:
            st.error("PDF was not generated ❌")

    except subprocess.CalledProcessError as e:
        st.error("LaTeX compilation failed ❌")
        st.text(e.stdout)
