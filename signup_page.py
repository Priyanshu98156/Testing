# import streamlit as st
# import time
# import firebase_admin

# from firebase_admin import auth
# from firebase_admin import credentials

# def render_signup_page():

#     st.title("Create a New Account")

#     with st.form("signup_form"):
#         username = st.text_input("Username*")
#         email = st.text_input("Email")
#         password = st.text_input("Password*", type="password")
#         confirm_password = st.text_input("Confirm Password*", type="password")
#         submitted = st.form_submit_button("Sign Up")

#         if submitted:
#             if not email or not password or not confirm_password:
#                 st.error("Please fill out all fields.")
#             elif password != confirm_password:
#                 st.error("Passwords do not match.")
#             else:
#                 try:
#                     user = auth.create_user(email=email, password=password)
#                     st.success(f"Account created for {user.email}! Please log in.")
#                     st.session_state.view = 'login' # Switch view back to login
#                     st.rerun()
#                 except Exception as e:
#                     st.error(f"Failed to create account: {e}")

#     st.write("---")
#     if st.button("Back to Login"):
#         st.session_state.view = 'login' # Switch view to login
#         st.rerun()


import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore

# ------------------ Firebase Initialization ------------------
def init_firebase():
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate("careercatalyst-225cb-e7cd4af759c0.json")
            firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Failed to initialize Firebase: {e}")

# Initialize Firebase
init_firebase()

# Firestore client (only works if Firestore exists)
try:
    db = firestore.client()
except Exception as e:
    st.warning("Firestore not initialized yet. Please create a Firestore database in your Firebase project.")
    db = None

# ------------------ Signup Page ------------------
def render_signup_page():
    st.title("Create a New Account")

    with st.form("signup_form"):
        name = st.text_input("Name*")
        email = st.text_input("Email*")
        password = st.text_input("Password*", type="password")
        confirm_password = st.text_input("Confirm Password*", type="password")
        submitted = st.form_submit_button("Sign Up")

        if submitted:
            if not name or not email or not password or not confirm_password:
                st.error("Please fill out all fields.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                try:
                    # Create user in Firebase Authentication
                    user = auth.create_user(
                        email=email,
                        password=password,
                        display_name=name
                    )

                    # Save additional data to Firestore if it exists
                    if db:
                        db.collection("users").document(user.uid).set({
                            "name": name,
                            "email": email
                        })

                    st.success(f"Account created for {user.email}! Please log in.")
                    st.session_state.view = 'login'
                    st.rerun()  # ✅ updated

                except Exception as e:
                    st.error(f"Failed to create account: {e}")

    st.write("---")
    if st.button("Back to Login"):
        st.session_state.view = 'login'
        st.rerun()  # ✅ updated

# ------------------ Main ------------------
if 'view' not in st.session_state:
    st.session_state.view = 'signup'

if st.session_state.view == 'signup':
    render_signup_page()
