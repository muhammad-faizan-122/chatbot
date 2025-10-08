from src.db.mongo.auth import AuthenticatorDb
from src.db.mongo.connection import get_database
from src.db.mongo.repository import MongoRepository
import streamlit as st


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
    if "db" not in st.session_state:
        st.session_state["db"] = get_database()
        print("db: ", st.session_state["db"])

    if "repo" not in st.session_state:
        st.session_state["repo"] = MongoRepository()
        print("repo: ", st.session_state["repo"])

    if "auth_db" not in st.session_state:
        st.session_state["auth_db"] = AuthenticatorDb(
            collection=st.session_state["db"]["users"],
            repo=st.session_state["repo"],
        )
        print("auth_db: ", st.session_state["auth_db"])


def reset_session():
    st.session_state["page"] = "login"
    st.session_state["guest_mode"] = False
    st.session_state["verifying"] = False
    st.session_state["otp"] = ""
    st.session_state["email"] = ""
    st.session_state["password"] = ""
    st.session_state["user_id"] = ""
    st.session_state["conversation_id"] = ""
