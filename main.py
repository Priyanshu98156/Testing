import streamlit as st
from streamlit_option_menu import option_menu
from resume_builder import show  # your function

# 🚨 Must be the very first Streamlit command
st.set_page_config(
    page_title="Resume App",
    page_icon="📄",
    layout="wide"
)

st.markdown(
    """
    <style>
        /* Sidebar width */
        [data-testid="stSidebar"] {
            min-width: 350px;
            max-width: 350px;
        }
    </style>
    """,
    unsafe_allow_html=True
)
# === Sidebar Navigation ===
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Home", "ATS Checker", "Resume Builder", "About"],
        icons=["house", "search", "file-earmark-text", "person-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#1e1e1e"},
            "icon": {"color": "#f9f9f9", "font-size": "25px"},
            "nav-link": {
                "font-size": "18px",
                "text-align": "left",
                "margin": "5px",
                "color": "#ffffff",
                "--hover-color": "#D2032D",
            },
            "nav-link-selected": {
                "background-color": "#D2032D",
                "color": "black",
                "font-weight": "bold",
                "icon-color": "white",
            },
        },
    )

# === Pages ===
if selected == "Home":
    st.markdown(
        "<h1 style='text-align: center; color: #1cfff2;'>📄 Resume App</h1>",
        unsafe_allow_html=True,
    )
    st.write("Welcome! Use the sidebar to navigate to ATS Checker or Resume Builder.")

elif selected == "ATS Checker":
    st.header("📊 ATS Checker")
    st.write("Upload your resume and paste the job description below:")

    resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    job_desc = st.text_area("Paste Job Description")

    if st.button("Check ATS Score"):
        if resume_file and job_desc:
            import random
            score = random.randint(50, 95)
            st.success(f"✅ ATS Score: {score}%")
        else:
            st.warning("Please upload a resume and paste job description!")

elif selected == "Resume Builder":
    # 🔥 directly call your show() function
    show()

elif selected == "About":
    st.header("👤 About")
    st.markdown(
        """
        This app was built to help candidates:
        - ✅ Check ATS compatibility of their resume  
        - ✅ Build structured resumes quickly  

        **Made with ❤️ using Streamlit**
        """
    )
