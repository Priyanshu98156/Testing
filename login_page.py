
import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

def render_login_page():
    st.markdown("""
        <style>
        /* Centered container like signup */
        .login-container {
            max-width: 600px;
            margin: 0rem auto;
            background: #0f2027;
            background: linear-gradient(135deg, #2c5364, #203a43, #0f2027);
            padding: 0rem;
            border-radius: 1.5rem;
            box-shadow: 0px 6px 20px rgba(0,0,0,0.3);
            color: #ffffff;
        }

        .login-container h1 {
            text-align: center;
            font-size: 3rem;
            color: #16ccc1;
            margin-bottom: 0.5rem;
        }

        .login-container h3 {
            text-align: center;
            color: #bbbbbb;
            font-size: 1.2rem;
            margin-bottom: 1.5rem;
        }

        .stTextInput > div > div > input {
            background-color: #1b1b1b;
            color: #ffffff;
            border-radius: 10px;
            border: 1px solid #333;
        }

        .stButton>button {
            width: 100%;
            background-color: #16ccc1;
            color: black;
            border-radius: 10px;
            font-weight: 600;
            margin-top: 1rem;
        }

        .stButton>button:hover {
            background-color: #13b2a9;
            color: white;
        }

        .signup-btn {
            text-align: left;
            margin-top: -1rem; /* pull it closer */
        }

        .signup-btn > button {
            width: auto;
            background-color: transparent;
            border: 1px solid #16ccc1;
            color: #16ccc1;
            border-radius: 10px;
            padding: 0.4rem 1rem;
        }

        .signup-btn > button:hover {
            background-color: #16ccc1;
            color: black;
        }
        </style>
    """, unsafe_allow_html=True)

    
    st.markdown("""
        <div class='login-container'>
            <h1>CareerCatalyst</h1>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3>🔑 Welcome Back — Log In to Continue</h3>", unsafe_allow_html=True)

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # Redirect if already logged in
    if st.session_state.logged_in:
        st.switch_page("home_page.py")

    with st.form("login_form"):
        email = st.text_input("Email*")
        password = st.text_input("Password*", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if email and password:
                try:
                    user = auth.get_user_by_email(email=email)
                    st.success("✅ Login successful!")
                    st.session_state.logged_in = True
                    st.session_state.view = 'home'
                    st.rerun()

                except auth.UserNotFoundError:
                    st.error("User not found. Please sign up.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.error("Please enter both email and password.")

    st.markdown("</div>", unsafe_allow_html=True)

        # Signup section beneath the form
    st.markdown("""
        <div style="text-align: left; margin-top: 1rem; color: #bbb;">
            <p>Don’t have an account?</p>
        </div>
    """, unsafe_allow_html=True)

    
    if st.button("Sign Up"):
        st.session_state.view = 'signup'
        st.rerun()
