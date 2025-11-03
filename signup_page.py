
####------------------ Firebase Initialization ------------------
# def init_firebase():
#     try:
#         if not firebase_admin._apps:
#             cred = credentials.Certificate("careercatalyst-b08ad-39759fa3a8f1.json")
#             firebase_admin.initialize_app(cred)
#     except Exception as e:
#         st.error(f"Failed to initialize Firebase: {e}")

# # Initialize Firebase
# init_firebase()

# ###Firestore client (only works if Firestore exists)
# try:
#     db = firestore.client()
# except Exception as e:
#     st.warning("Firestore not initialized yet. Please create a Firestore database in your Firebase project.")
#     db = None

# ------------------ Signup Page ------------------
import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore

def render_signup_page():
    st.markdown("""
        <style>
        /* Center the form nicely */
        .signup-container {
            max-width: 600px;
            margin: 0rem auto;
            background: #0f2027;
            background: linear-gradient(135deg, #2c5364, #203a43, #0f2027);
            padding: 0rem ;
            border-radius: 1.5rem;
            box-shadow: 0px 6px 20px rgba(0,0,0,0.3);
            color: #ffffff;
        }

        .signup-container h1 {
            text-align: center;
            margin-bottom: 1rem;
            font-size: 3rem;
            color: #16ccc1;
        }

        .signup-container p {
            text-align: center;
            color: #bbbbbb;
            font-size: 0.95rem;
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

        .stTextInput label {
            color: #ddd;
            font-weight: 500;
        }

        .back-btn > button {
            width: 100%;
            background-color: transparent;
            border: 1px solid #16ccc1;
            color: #16ccc1;
            border-radius: 10px;
            margin-top: 0.5rem;
        }

        .back-btn > button:hover {
            background-color: #16ccc1;
            color: black;
        }
        </style>
    """, unsafe_allow_html=True)
    #  Add heading + intro text
    # st.markdown("""
    #     <div class='signup-container'>
    #         <h1>CareerCatalyst</h1>
    # """, unsafe_allow_html=True)
    st.markdown("<h3>🔐 Create Your Account</h1>", unsafe_allow_html=True)

    db = firestore.client()
    try:
        db = firestore.client()
    except Exception as e:
        st.warning("⚠️ Firestore not initialized. Please create a Firestore database in your Firebase project.")
        db = None

    with st.form("signup_form"):
        name = st.text_input("Full Name*")
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
                    user = auth.create_user(
                        email=email,
                        password=password,
                        display_name=name
                    )

                    if db:
                        db.collection("users").document(user.uid).set({
                            "name": name,
                            "email": email
                        })

                    st.success(f"✅ Account created for {user.email}! Please log in.")
                    st.session_state.view = 'login'
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Failed to create account: {e}")

    st.markdown("</div>", unsafe_allow_html=True)
    # st.write("")
    # Back to Login button (left aligned, below form)
    st.markdown("""
        <div style="text-align: left; margin-top: 1rem; color: #bbb;">
            <p>Already have an account?</p>
        </div>
    """, unsafe_allow_html=True)
    # st.markdown("""
    #     <div class='back-btn' style='text-align: left; margin-left: 0rem; margin-top: -0.3rem;'>
    # """, unsafe_allow_html=True)

    if st.button("← Login"):
        st.session_state.view = 'login'
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

