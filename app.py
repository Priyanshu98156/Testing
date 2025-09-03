import streamlit as st
import subprocess
import os
from jinja2 import Environment, FileSystemLoader
from api_calls import generate_resume_summary
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
if "projects" not in st.session_state:
    st.session_state["projects"] = []

job_desc        = st.text_input("Enter job description")
user_summary    = st.text_input("Enter your summary")

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
languages          = st.text_input("Languages", placeholder="e.g., c++,Python");
tools              = st.text_input("Tools ", placeholder="e.g., VSCode");
frameworks         = st.text_input("Frameworks ", placeholder="e.g.,React,NodeJs");
certificates       = st.text_input("Enter your certificates (comma separated)", placeholder= "e.g., Mastering DSA- Udemy , Machine learning using Python-Udemy")
st.header("Projects")

with st.form("project_form", clear_on_submit=True):
    proj_name = st.text_input("Project Name")
    proj_link = st.text_input("Project Link (GitHub/Live/Download)")
    proj_stack = st.text_input("Technology Stack")
    proj_points = st.text_area("Key Points (comma separated)")
    proj_date = st.text_input("Date (MM YYYY)")
    
    submitted = st.form_submit_button("Add Project")
    if submitted:
        st.session_state["projects"].append({
            "name": proj_name,
            "link": proj_link,
            "stack": proj_stack,
            "points": [p.strip() for p in proj_points.split(",") if p.strip()],
            "date": proj_date
        })

# Show projects already added
for i, proj in enumerate(st.session_state["projects"]):
    st.markdown(f"**{proj['name']}** ({proj['date']}) — {proj['stack']}")
    for p in proj["points"]:
        st.markdown(f"- {p}")


if certificates:
    cert_list = [c.strip() for c in certificates.split(",")]

    certs_latex = "\n".join(
        [fr"$\sbullet[.75] \hspace{{0.1cm}}$ {c} \\" for c in cert_list]
    )


def generate_projects_latex(projects):
    project_latex = ""
    for proj in projects:
        # Create bullet points for the project
        bullets = "\n".join([fr"\item {p}" for p in proj["points"]])
        
        # Each project block
        project_latex += (
            fr"\textbf{{{proj['name']}}} "
            fr"\href{{{proj['link']}}}{{\faExternalLink}} "
            fr"| \textit{{{proj['stack']}}} \hfill {proj['date']} \\[2pt]"  # small vertical space
            "\n"
            r"\begin{itemize}[leftmargin=*]" "\n"
            f"{bullets}" "\n"
            r"\end{itemize}" "\n\n"
        )
    return project_latex


if st.button("Generate Resume"):
    try:
        # Load Jinja2 template and render with user input
        polished_summary = generate_resume_summary( job_desc, user_summary)
        projects_latex = generate_projects_latex(st.session_state["projects"])
        template = env.get_template("resume.tex")
        latex_code = template.render(
            name=name,
            telephone=phone,
            email=email,
            linkedin=linkedin,
            github=github,
            city=city,
            user_summary = polished_summary,
            grad_college = grad_college,
            grad_batch_start =  grad_batch_start,
            grad_name = grad_name,
            grad_cgpa = grad_cgpa,
            grad_batch_end = grad_batch_end,
            grad_city_state = grad_city_state,
            languages=languages,
            tools=tools,
            frameworks=frameworks,
            certs_latex=certs_latex,
            projects_latex = projects_latex

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
