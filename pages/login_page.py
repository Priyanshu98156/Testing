import streamlit as st
import firebase_admin

from firebase_admin import auth
from firebase_admin import credentials

# cred = credentials.Certificate("careercatalyst-74196-d3e6a59f2546.json")
# firebase_admin.initialize_app(cred)




st.set_page_config(page_title="Login")

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Redirect if already logged in
if st.session_state.logged_in:
    st.switch_page("pages/home_page.py")

st.title("Login")

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
                st.success(f"Login successful for user: {email}. Redirecting to Home...")
                st.switch_page("pages/home_page.py")
                
            except Exception as e:
                print("errror", e) 
            
        else:
            st.error("Invalid username or password.")

st.write("---")
st.write("Don't have an account?")
if st.button("Sign Up"):
    st.switch_page("pages/signup_page.py")





