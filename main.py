import streamlit as st
import firebase_admin
from firebase_admin import credentials
import os
from firebase_admin import auth


from home_page import render_home_page
from login_page import render_login_page
from signup_page import render_signup_page

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="App",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- GLOBAL STATE & FIREBASE ---
# Initialize session state variables.
if "view" not in st.session_state:
    st.session_state.view = 'splash'
    st.session_state.logged_in = False
    st.session_state.firebase_initialized = False

def initialize_firebase():
    """Initializes the Firebase Admin SDK, ensuring it only runs once."""
    if not st.session_state.firebase_initialized:
        try:
            key_path = "careercatalyst-b08ad-39759fa3a8f1.json" # Your key file
            if os.path.exists(key_path):
                cred = credentials.Certificate(key_path)
                firebase_admin.initialize_app(cred)
                st.session_state.firebase_initialized = True
                print("✅ Firebase initialized.")
            else:
                st.error("Firebase credentials file not found.")
                st.stop()
        except Exception as e:
            st.error(f"Failed to initialize Firebase: {e}")
            st.stop()

# --- MAIN APP ROUTER ---
# This is the core logic that decides which 'page' or 'view' to show.

# 1. Splash Screen View
if st.session_state.view == 'splash':
    with st.spinner("Starting up..."):
        initialize_firebase()
    # After initialization, switch to the login view and rerun the script
    st.session_state.view = 'login'
    st.rerun()

# 2. Login View
elif st.session_state.view == 'login':
    render_login_page()

# 3. Signup View
elif st.session_state.view == 'signup':
    render_signup_page()

# 4. Home View (after successful login)
elif st.session_state.view == 'home':
    # This view is protected. If not logged in, redirect to login.
    if not st.session_state.logged_in:
        st.warning("Please log in to continue.")
        st.session_state.view = 'login'
        st.rerun()
    else:
        render_home_page()







