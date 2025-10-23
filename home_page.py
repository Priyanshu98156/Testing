import streamlit as st
from streamlit_option_menu import option_menu
from resume_builder import show  # your function
import videores
from ats_checker import ats_checker
# 🚨 Must be the very first Streamlit command

def render_home_page():

    st.set_page_config(
        page_title="Career Catalyst",
        # page_icon="📄",
        layout="wide"
    )
#     st.markdown(
#     """
#     <style>
#         /* Change main app background */
#         .stApp {
#             background-color: #D3C5C5;  /* Dark background */
#             color: black;  /* Text color for contrast */
#         }

#         /* Optional: Customize text inputs, buttons, etc. */
#         .stTextInput > div > div > input {
#             background-color: #1a1d23;
#             color: white;
#         }

#         .stButton > button {
#             background-color: #2b313e;
#             color: white;
#             border-radius: 10px;
#         }

#         .stButton > button:hover {
#             background-color: #4b5563;
#             color: white;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )


    
    # === Sidebar Navigation ===
    with st.sidebar:
        selected = option_menu(
            menu_title="Navigation",
            options=["Home", "ATS Checker", "Resume Builder", "About"],
            icons=["house", "search", "file-earmark-text", "person-circle"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "#000000"},
                "icon": {"color": "#D3C5C5", "font-size": "25px"},
                "nav-link": {
                    "font-size": "18px",
                    "text-align": "left",
                    "margin": "5px",
                    "color": "#ffffff",
                    "--hover-color": "#38393c",
                },
                "nav-link-selected": {
                    "background-color": "#38393c",
                    "color": "black",
                    "font-weight": "bold",
                    "icon-color": "white",
                },
            },
        )

    # === Pages ===
    if selected == "Home":
        st.markdown("""
            <h1 style='text-align: center; color: #16ccc1; font-size: 60px; font-weight:bold;'>CareerCatalyst</h1>
            <p style='text-align: center; color: #16ccc1    ; font-size: 18px;'>AI-powered resume matcher and career guide</p>
        """, unsafe_allow_html=True)
        # st.write("Welcome! Use the sidebar to navigate to ATS Checker or Resume Builder.")

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

            **Made with ❤️ using Streamlit**
            """
        )
