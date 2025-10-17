import streamlit as st
import firebase_admin

from firebase_admin import auth
from firebase_admin import credentials

# cred = credentials.Certificate("careercatalyst-74196-d3e6a59f2546.json")
# firebase_admin.initialize_app(cred)


def render_login_page():
    # Session state for login
    st.title("Login")
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # Redirect if already logged in
    if st.session_state.logged_in:
        st.switch_page("home_page.py")


    with st.form("login_form"):
        email = st.text_input("email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            # 🔹 Replace this with your actual authentication logic
            if email and password:
                try:
                    user = auth.get_user_by_email(email = email)
                    print("✅ Login successful!")
                    
                    st.session_state.logged_in = True
                    st.session_state.view = 'home'
                    st.rerun()
                    
                except auth.UserNotFoundError:
                    st.error("User not found. Please sign up.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.error("Please enter both email and password.")

    st.write("---")
    st.write("Don't have an account?")
    if st.button("Sign Up"):
        st.session_state.view = 'signup'
        st.rerun()





