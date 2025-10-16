import streamlit as st
import time
import firebase_admin

from firebase_admin import auth
from firebase_admin import credentials
# cred = credentials.Certificate("careercatalyst-74196-d3e6a59f2546.json")
# firebase_admin.initialize_app(cred)

st.set_page_config(page_title="Signup Page")

st.title("Sign Up")

with st.form("signup_form"):
    username = st.text_input("Username*")
    email = st.text_input("Email*")
    password = st.text_input("Password*", type="password")
    confirm_password = st.text_input("Confirm Password*", type="password")
    submitted = st.form_submit_button("Sign Up")

    if submitted:
        if password == confirm_password and password:
            try:
                user = auth.create_user( email = email, password = confirm_password)
                st.success(f"Account created for {username}. Redirecting to login page...")
                time.sleep(2)
                st.switch_page("pages/login_page.py")
            except Exception as e:
                print(e)

        elif not password:
            st.error("Password cannot be empty.")
        else:
            st.error("Passwords do not match.")

st.write("---")
st.write("Already have an account?")
if st.button("Go to Login"):
    st.switch_page("pages/login_page.py")




#  auth.create_user(
    #     email=email, password=password, display_name=name, email_verified=False
    # )