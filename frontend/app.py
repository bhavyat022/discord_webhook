import streamlit as st
import requests
from supabase import create_client, Client


import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

st.title("Send a message notification to discord.")

if "session" not in st.session_state:
    st.session_state.session = None

if not st.session_state.session:
    auth_choice = st.radio("Login or Sign Up", ["Login", "Sign Up"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button(auth_choice):
        try:
            if auth_choice == "Login":
                user = supabase.auth.sign_in_with_password({"email": email, "password": password})
            elif auth_choice == "Sign Up":
                user = supabase.auth.sign_up({"email": email, "password": password})

                # Check if user already exists in users table before inserting
                existing_user = supabase.table("users").select("id").eq("id", user.user.id).execute()
                if not existing_user.data:
                    supabase.table("users").insert({"id": user.user.id, "email": email}).execute()
            else:
                user = supabase.auth.sign_up({"email": email, "password": password})
            st.session_state.session = user
            st.success("Authenticated!")
        except Exception as e:
            st.error(str(e))
else:
    st.success(f"Logged in as {st.session_state.session.user.email}")
    message = st.text_area("Type your message here")
    if st.button("Send"):
        response = requests.post("http://127.0.0.1:8000/send", json={
            "email": st.session_state.session.user.email,
            "content": message
        })
        
        st.success("Message sent!")
        st.success("Message sent! Check Discord.")
        

    if st.button("Logout"):
        st.session_state.session = None