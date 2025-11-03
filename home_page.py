import streamlit as st
from streamlit_option_menu import option_menu
from resume_builder import show  # your function
import videores
from ats_checker import ats_checker
# 🚨 Must be the very first Streamlit command
from urllib.parse import urlparse, parse_qs

from urllib.parse import urlparse, parse_qs

query_params = st.query_params
if "selected_page" in query_params:
    st.session_state["selected_page"] = query_params["selected_page"]
    st.rerun()   # <--- 🔥 rerun immediately so the page updates
elif "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Home"

def render_home_page():

    st.set_page_config(
        page_title="Career Catalyst",
        # page_icon="📄",
        layout="wide"
    )
    st.markdown("""
        <style>
        /* 🔥 Change entire sidebar background */
        [data-testid="stSidebar"] {
            background: linear-gradient(10deg, #000000, #1a1a1a);  /* You can use solid color or gradient */
            color: white;
        }

        /* Optional: tweak the sidebar text & icons */
        [data-testid="stSidebar"] * {
            color: #16ccc1 !important;  /* This makes all text/icons light aqua */
        }
        </style>
    """, unsafe_allow_html=True)



    st.markdown("""
    <style>
    /* 🔥 Set full app background */
    .stApp {
        background-color: #000000;   /* Change this to any color you want */
    }
    </style>
""", unsafe_allow_html=True)

    
    # === Sidebar Navigation ===
    with st.sidebar:
        selected_sidebar = option_menu(
            menu_title="Navigation",
            options=["Home", "ATS Checker", "Resume Builder", "About"],
            icons=["house", "search", "file-earmark-text", "person-circle"],
            menu_icon="cast",
            default_index=0,
            styles={
                 
                "container": {"padding": "5px", "background-color": "#000000"},#small container color
                "icon": {"color": "#D3C5C5", "font-size": "25px"},
                "nav-link": {
                    "font-size": "18px",
                    "text-align": "left",
                    "margin": "5px",
                    "color": "#ffffff",
                    "--hover-color": "#0f2027",
                },
                "nav-link-selected": {
                    "background-color": "#38393c",#hover color
                    "color": "black",
                    "font-weight": "bold",
                    "icon-color": "white",
                },
            },
        )
    st.session_state["selected_page"] = selected_sidebar
    selected = st.session_state["selected_page"]

    # === Pages ===
    if selected == "Home":
        
        st.markdown("""
            <style>
            .main-container {
                text-align: center;
                padding: 80px 20px;
                background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
                color: white;
                border-radius: 15px;
                margin-bottom: 60px; 
            }

            .main-title {
                font-size: 70px;
                font-weight: 900;
                background: linear-gradient(90deg, #16ccc1, #00bfa5, #1de9b6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .subtitle {
                font-size: 22px;
                color: #dcdcdc;
                margin-top: -10px;
                margin-bottom: 50px;
            }

            .feature-card {
                background-color: rgba(255, 255, 255, 0.05);
                padding: 25px;
                border-radius: 15px;
                text-align: center;
                transition: 0.3s;
            }
            .feature-card:hover {
                transform: translateY(-8px);
                background-color: rgba(255, 255, 255, 0.1);
            }

            .feature-icon {
                font-size: 40px;
                margin-bottom: 10px;
                color: #16ccc1;
            }
            </style>

            <div class='main-container'>
                <h1 class='main-title'>Career Catalyst</h1>
                <p class='subtitle'>AI-powered resume matcher & career companion</p>
            </div>
        """, unsafe_allow_html=True)

        # --- Feature Cards Layout ---
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
                <style>
                .clickable-card {
                    background-color: rgba(255, 255, 255, 0.05);
                    padding: 25px;
                    border-radius: 15px;
                    text-align: center;
                    transition: 0.3s;
                    cursor: pointer;
                    text-decoration: none !important;
                    display: block;
                    color: inherit !important; /* 🔥 keeps text color same */
                }

                .clickable-card:hover {
                    transform: translateY(-8px);
                    background-color: rgba(255, 255, 255, 0.1);
                }

                .clickable-card h3,
                .clickable-card p {
                    color: white !important; /* ensures text stays white */
                }

                .feature-icon {
                    font-size: 40px;
                    margin-bottom: 10px;
                    color: #16ccc1;
                }

                a {
                    text-decoration: none !important; /* removes blue underline globally */
                    color: inherit !important; /* ensures no blue text */
                }
                </style>

                <a href="?selected_page=ATS Checker" target="_self" class="clickable-card">
                    <div class='feature-icon'>🧠</div>
                    <h3>ATS Checker</h3>
                    <p>Upload your resume & job description. Get instant ATS match insights.</p>
                </a>
            """, unsafe_allow_html=True)



        with col2:
            st.markdown("""
                <div class='feature-card'>
                    <div class='feature-icon'>📝</div>
                    <h3>Resume Builder</h3>
                    <p>Create a sleek, recruiter-ready resume tailored for your dream role.</p>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
                <div class='feature-card'>
                    <div class='feature-icon'>🚀</div>
                    <h3>Career Growth</h3>
                    <p>Use AI insights to polish your profile and boost your hiring chances.</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)
        


    elif selected == "ATS Checker":
        ats_checker()

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

            
            """
        )

