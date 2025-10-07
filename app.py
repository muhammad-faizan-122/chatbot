from src.pages.utils.session_states import init_session, reset_session
from src.pages.login import login_page
from src.pages.signup import signup_page
from src.pages.chat import app_page
import streamlit as st


init_session()

if st.session_state["authenticated"]:
    app_page()

else:
    if st.session_state["page"] == "login":
        reset_session()
        login_page(guest_mode=True)

    elif st.session_state["page"] == "signup":
        signup_page(confirmPass=True)
