


# -----------------------------------------------------------------------------------------------------------------------------------------
import streamlit as st
import subprocess
import os
from jinja2 import Environment, FileSystemLoader
from api_calls import generate_resume_summary, generate_project_summary


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
# Escape LaTeX special characters

def escape_latex(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "%": r"\%",
        "&": r"\&",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.replace("\n", r"\\ ")


# Register as Jinja filter

env.filters["latex_escape"] = escape_latex


st.title("Resume Generator (LaTeX via TeX Live)")

# Inputs
if "projects" not in st.session_state:
    st.session_state["projects"] = []
if "education" not in st.session_state:
    st.session_state["education"] = []
if "skills" not in st.session_state:
    st.session_state["skills"] = []

if "personal_info" not in st.session_state:
    st.session_state["personal_info"] = {}


# job_desc        = st.text_input("Enter job description")
# user_summary    = st.text_input("Enter your summary")
st.header("Job Description & Summary")

if "jd_summary" not in st.session_state:
    st.session_state["jd_summary"] = {"jd": "", "summary": ""}

with st.form("jd_summary_form"):
    jd_text = st.text_area(
        "Job Description", 
        value=st.session_state["jd_summary"]["jd"], 
        placeholder="Paste the job description here..."
    )
    summary_text = st.text_area(
        "Your Summary", 
        value=st.session_state["jd_summary"]["summary"], 
        placeholder="Write about your profile..."
    )

    submitted_jd = st.form_submit_button("Save JD & Summary")

    if submitted_jd:
        st.session_state["jd_summary"]["jd"] = jd_text
        st.session_state["jd_summary"]["summary"] = summary_text
        st.success("Job description & summary saved ✅")

if st.session_state["jd_summary"]["jd"] or st.session_state["jd_summary"]["summary"]:
    st.markdown("---")
    st.subheader("📌 Job Description")
    st.write(st.session_state["jd_summary"]["jd"])

    st.subheader("📝 Summary")
    st.write(st.session_state["jd_summary"]["summary"])
    st.markdown("---")














st.header("Personal Information")


with st.form("personal_info_form"):
    st.write("Enter your personal details:")
    name = st.text_input("Full Name", value=st.session_state["personal_info"].get("name", ""), placeholder="e.g., Priyansh Sharma")
    phone = st.text_input("Phone Number", value=st.session_state["personal_info"].get("phone", ""), placeholder="e.g., +91 9876543210")
    email = st.text_input("Email Address", value=st.session_state["personal_info"].get("email", ""), placeholder="e.g., you@example.com")
    linkedin = st.text_input("LinkedIn Profile URL", value=st.session_state["personal_info"].get("linkedin", ""), placeholder="e.g., https://linkedin.com/in/username")
    github = st.text_input("GitHub Profile URL", value=st.session_state["personal_info"].get("github", ""), placeholder="e.g., https://github.com/username")
    city = st.text_input("City", value=st.session_state["personal_info"].get("city", ""), placeholder="e.g., New Delhi")

    submitted_info = st.form_submit_button("Save Personal Information")

    if submitted_info:
        st.session_state["personal_info"] = {
            "name": name,
            "phone": phone,
            "email": email,
            "linkedin": linkedin,
            "github": github,
            "city": city
        }
        st.success("Personal information saved! ✅")

if st.session_state["personal_info"]:
    info = st.session_state["personal_info"]
    st.markdown("---")
    st.markdown(f"**Name:** {info['name']}")
    st.markdown(f"**Contact:** {info['phone']} | {info['email']}")
    st.markdown(f"**Links:** [LinkedIn]({info['linkedin']}) | [GitHub]({info['github']})")
    st.markdown(f"**Location:** {info['city']}")
    st.markdown("---")

# name     = st.text_input("Full Name", placeholder="e.g., Priyanshu Sharma")
# phone    = st.text_input("Phone Number", placeholder="e.g., +91 9876543210")
# email    = st.text_input("Email Address", placeholder="e.g., you@example.com")
# linkedin = st.text_input("LinkedIn Profile URL", placeholder="e.g., https://linkedin.com/in/username")
# github   = st.text_input("GitHub Profile URL", placeholder="e.g., https://github.com/username")
# city     = st.text_input("City", placeholder="e.g., New Delhi")



st.header("Education")

with st.form("education_form", clear_on_submit=True):
    edu_degree = st.text_input("Degree", placeholder="e.g., B.Tech in Computer Science")
    edu_institute = st.text_input("Institute / University", placeholder="e.g., DAV Institute of Engineering & Technology")
    edu_city_state = st.text_input("City, State", placeholder="e.g., Jalandhar, Punjab")
    edu_score = st.text_input("CGPA / Percentage", placeholder="e.g., 8.2/10 or 82%")
    edu_start = st.text_input("Start Date", placeholder="e.g., Aug 2022")
    edu_end = st.text_input("End Date", placeholder="e.g., June 2026")

    submitted_edu = st.form_submit_button("Add Education")
    if submitted_edu:
        st.session_state["education"].append({
            "degree": edu_degree,
            "institute": edu_institute,
            "city_state": edu_city_state,
            "score": edu_score,
            "start": edu_start,
            "end": edu_end
        })
for edu in st.session_state["education"]:
    st.markdown(
        f"**{edu['degree']}** — {edu['institute']} ({edu['city_state']})  "
        f"📅 {edu['start']} - {edu['end']}  "
        f"🎯 {edu['score']}"
    )
def generate_education_latex(education_list):
    edu_latex = ""
    for edu in education_list:
        edu_latex += (
            fr"\textbf{{{edu['degree']}}} \hfill {edu['start']} -- {edu['end']} \\[2pt]" "\n"
            fr"{edu['institute']}, {edu['city_state']} \hfill {edu['score']} \\[6pt]" "\n\n"
        )
    return edu_latex


st.header("Technical Skills")

with st.form("skills_form", clear_on_submit=True):
    skill_category = st.selectbox(
        "Skill Category",
        ["Languages", "Frameworks", "Tools", "Other"]
    )
    skill_name = st.text_input("Skill", placeholder="e.g., Python, React, Git")

    submitted_skill = st.form_submit_button("Add Skill")
    if submitted_skill:
        st.session_state["skills"].append({
            "category": skill_category,
            "name": skill_name
        })
if st.session_state["skills"]:
    st.subheader("📌 Added Skills")
    for skill in st.session_state["skills"]:
        st.markdown(f"- **{skill['category']}**: {skill['name']}")

from collections import defaultdict

def generate_skills_latex(skills):
    grouped = defaultdict(list)
    for s in skills:
        grouped[s["category"]].append(s["name"])

    latex_output = ""
    for category, items in grouped.items():
        joined = ", ".join(items)
        latex_output += fr"\textbf{{{category}}}: {joined} \\[4pt]" "\n"
    return latex_output



st.header("Certifications")
certificates       = st.text_input("Enter your certificates (comma separated)", placeholder= "e.g., Mastering DSA- Udemy , Machine learning using Python-Udemy")


st.header("Projects")



# with st.form("project_form", clear_on_submit=True):
#     proj_name = st.text_input("Project Name")
#     proj_link = st.text_input("Project Link (GitHub/Live/Download)")
#     proj_stack = st.text_input("Technology Stack")
#     proj_points = st.text_area("Key Points (comma separated)")
#     proj_date = st.text_input("Date (MM YYYY)")
    
#     submitted = st.form_submit_button("Add Project")
#     if submitted:
#         st.session_state["projects"].append({
#             "name": proj_name,
#             "link": proj_link,
#             "stack": proj_stack,
#             "points": [p.strip() for p in proj_points.split(",") if p.strip()],
#             "date": proj_date
#         })

with st.form("project_form", clear_on_submit=True):
    proj_name = st.text_input("Project Name")
    proj_link = st.text_input("Project Link (GitHub/Live/Download)")
    proj_stack = st.text_input("Technology Stack")
    proj_raw_summary = st.text_area("Short Project Description (1–2 lines)")
    proj_points = st.text_area("Key Points (comma separated)")
    proj_date = st.text_input("Date (MM YYYY)")

    submitted = st.form_submit_button("Add Project")
    if submitted:
        # ✅ Call Gemini API for polished summary
        polished_proj_summary = generate_project_summary(proj_name, proj_raw_summary)

        st.session_state["projects"].append({
            "name": proj_name,
            "link": proj_link,
            "stack": proj_stack,
            "summary": polished_proj_summary,   # store polished summary
            "points": [p.strip() for p in proj_points.split(",") if p.strip()],
            "date": proj_date
        })
        st.success(f"Project '{proj_name}' added with polished summary! ✅")


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


# def generate_projects_latex(projects):
#     project_latex = ""
#     for proj in projects:
#         # Create bullet points for the project
#         bullets = "\n".join([fr"\item {p}" for p in proj["points"]])
        
#         # Each project block
#         project_latex += (
#             fr"\textbf{{{proj['name']}}} "
#             fr"\href{{{proj['link']}}}{{\faExternalLink}} "
#             fr"| \textit{{{proj['stack']}}} \hfill {proj['date']} \\[2pt]"  # small vertical space
#             "\n"
#             r"\begin{itemize}[leftmargin=*]" "\n"
#             f"{bullets}" "\n"
#             r"\end{itemize}" "\n\n"
#         )
#     return project_latex
def generate_projects_latex(projects):
    project_latex = ""
    for proj in projects:
        bullets = "\n".join([fr"\item {p}" for p in proj["points"] if p.strip()])

        project_latex += (
            fr"\textbf{{{proj['name']}}} "
            fr"\href{{{proj['link']}}}{{\faExternalLink}} "
            fr"| \textit{{{proj['stack']}}} \hfill {proj['date']} \\[2pt]" "\n"
            fr"{proj['summary']} \\[4pt]" "\n"
        )
        

        if bullets:  # ✅ Only add itemize if points exist
            project_latex += (
                r"\begin{itemize}[leftmargin=*]" "\n"
                f"{bullets}" "\n"
                r"\end{itemize}" "\n\n"
            )

    return project_latex




if st.button("Generate Resume"):
    try:
        # Check if required information is present
        if not st.session_state["personal_info"]:
            st.error("Please fill out and save your personal information.")
           

        if not st.session_state["education"]:
            st.error("Please add at least one education entry.")
            

        # Access data from session_state
        info = st.session_state["personal_info"]

        # Call the polish summary API (if you have one)
        # Replace direct job_desc and user_summary with saved state
        job_desc = st.session_state["jd_summary"]["jd"]
        user_summary = st.session_state["jd_summary"]["summary"]

# Call API to polish the summary
        polished_summary = generate_resume_summary(job_desc, user_summary)

        
        # Generate LaTeX code for sections
        projects_latex = generate_projects_latex(st.session_state["projects"])
        education_latex = generate_education_latex(st.session_state["education"])
        skills_latex = generate_skills_latex(st.session_state["skills"])
        certs_latex = "\n".join([fr"$\sbullet[.75] \hspace{{0.1cm}}$ {c} \\" for c in [c.strip() for c in certificates.split(",")] if c.strip()])

        # Load Jinja2 template and render with all data
        template = env.get_template("resume.tex")
        latex_code = template.render(
            name=info['name'],
            telephone=info['phone'],
            email=info['email'],
            linkedin=info['linkedin'],
            github=info['github'],
            city=info['city'],
            user_summary=polished_summary,
            certs_latex=certs_latex,
            projects_latex=projects_latex,
            education_latex=education_latex,
            skills_latex=skills_latex
        )

        # Write and compile the LaTeX file
        tex_file = "resumefinal.tex"
        pdf_file = "resumefinal.pdf"

        with open(tex_file, "w", encoding="utf-8") as f:
            f.write(latex_code)

        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Handle compilation output
        if result.returncode != 0:
            st.error("LaTeX compilation failed ❌")
            st.text(result.stdout)
            st.text(result.stderr)
        elif os.path.exists(pdf_file):
            st.success("PDF generated successfully ✅")
            with open(pdf_file, "rb") as f:
                st.download_button("Download Resume", f, file_name=f"{name}Resume.pdf")
        else:
            st.error("PDF was not generated ❌")

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")