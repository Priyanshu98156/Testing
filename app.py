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

st.title("Resume Generator (LaTeX via TeX Live)")

# Inputs
name = st.text_input("Enter your name")
telephone = st.text_input("Enter your phone number")
email = st.text_input("Enter your email")
linkedin = st.text_input("Enter your LinkedIn URL")
github = st.text_input("Enter your GitHub URL")
hackerrank_id = st.text_input("Enter your Hackerrank URL")
city = st.text_input("Enter your city")

if st.button("Generate Resume"):
    try:
        # Load Jinja2 template and render with user input
        template = env.get_template("resume.tex")
        latex_code = template.render(
            name=name,
            telephone=telephone,
            email=email,
            linkedin=linkedin,
            github=github,
            hackerrank_id=hackerrank_id,
            city=city
        )

        tex_file = "resumefinal.tex"
        pdf_file = "resumefinal.pdf"

        # Save final LaTeX file
        with open(tex_file, "w", encoding="utf-8") as f:
            f.write(latex_code)

        # Compile LaTeX using pdflatex (comes from TeX Live)
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            st.error("LaTeX compilation failed ❌")
            st.text(result.stdout)
            st.text(result.stderr)
        elif os.path.exists(pdf_file):
            st.success("PDF generated successfully ✅")
            with open(pdf_file, "rb") as f:
                st.download_button("Download Resume", f, file_name="resume.pdf")
        else:
            st.error("PDF was not generated ❌")

    except Exception as e:
        st.error(f"Unexpected error: {e}")
