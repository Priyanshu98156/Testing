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
name     = st.text_input("Full Name", placeholder="e.g., Priyanshu Sharma")
phone    = st.text_input("Phone Number", placeholder="e.g., +91 9876543210")
email    = st.text_input("Email Address", placeholder="e.g., you@example.com")
linkedin = st.text_input("LinkedIn Profile URL", placeholder="e.g., https://linkedin.com/in/username")
github   = st.text_input("GitHub Profile URL", placeholder="e.g., https://github.com/username")
city     = st.text_input("City", placeholder="e.g., New Delhi")

grad_name          = st.text_input("Graduation Name", placeholder="e.g., B.tech")
grad_cgpa          = st.text_input("Graduation CGPA / Percentage", placeholder="e.g., 8.2/10 or 82%")
grad_college       = st.text_input("Graduation College", placeholder="e.g., DAV Institute of Engineering & Technology")
grad_batch_start   = st.text_input("Enter Start of Graduation ", placeholder="e.g., Aug 2022")
grad_batch_end     = st.text_input("Enter End of Graduation ", placeholder="e.g., June 2026")
grad_city_state    = st.text_input("Enter State, City of Gradation College ", placeholder="e.g., Jalandhar, Punjab");
languages   = st.text_input("Languages", placeholder="e.g., c++,Python");
tools    = st.text_input("Tools ", placeholder="e.g., VSCode");
frameworks= st.text_input("Frameworks ", placeholder="e.g.,React,NodeJs");
certificates = st.text_input("Certifications", placeholder="e.g., ReactJS & Redux - Udemy, SQL, Java")

# if certificates.strip():
#     certificates_list = "".join([f"\\item {c.strip()}\n" for c in certificates.split(",") if c.strip()])
# else:
#     certificates_list = "\\item None"   # fallback so LaTeX doesn't break



if st.button("Generate Resume"):
    try:
        # Load Jinja2 template and render with user input
        template = env.get_template("resume.tex")
        latex_code = template.render(
            name=name,
            telephone=phone,
            email=email,
            linkedin=linkedin,
            github=github,
            city=city,
            grad_college = grad_college,
            grad_batch_start =  grad_batch_start,
            grad_name = grad_name,
            grad_cgpa = grad_cgpa,
            grad_batch_end = grad_batch_end,
            grad_city_state = grad_city_state,
            languages=languages,
            tools=tools,
            frameworks=frameworks,
            certificates=certificates

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
                st.download_button("Download Resume", f, file_name=f"{name}.pdf")
        else:
            st.error("PDF was not generated ❌")

    except Exception as e:
        st.error(f"Unexpected error: {e}")
