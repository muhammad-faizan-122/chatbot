import streamlit as st
from src.db.mongodb import AuthenticatorDb


def init_session():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "page" not in st.session_state:
        st.session_state["page"] = "login"
    if "guest_mode" not in st.session_state:
        st.session_state["guest_mode"] = False
    if "verifying" not in st.session_state:
        st.session_state["verifying"] = False
    if "otp" not in st.session_state:
        st.session_state["otp"] = ""
    if "email" not in st.session_state:
        st.session_state["email"] = ""
    if "password" not in st.session_state:
        st.session_state["password"] = ""
    if "auth_db" not in st.session_state:
        st.session_state["auth_db"] = AuthenticatorDb(collection_name="users")


def reset_session():
    st.session_state["page"] = "login"
    st.session_state["guest_mode"] = False
    st.session_state["verifying"] = False
    st.session_state["otp"] = ""
    st.session_state["email"] = ""
    st.session_state["password"] = ""
    st.session_state["user_id"] = ""
    st.session_state["conversation_id"] = ""
