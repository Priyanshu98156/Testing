import streamlit as st 
import firebase_admin

from firebase_admin import auth
from firebase_admin import credentials

cred = credentials.Certificate("careercatalyst-74196-d3e6a59f2546.json")
firebase_admin.initialize_app(cred)


st.switch_page("pages/login_page.py")