import streamlit as st
import re
import time


def is_valid_email(email):
    """Check if the provided email is valid using regex."""
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, email) is not None


def signup_page(confirmPass=False):
    """Render the signup page with optional extra input parameters and password confirmation."""
    if st.session_state["verifying"]:

        # Check if the user already exists
        if st.session_state["auth_db"].verify_duplicate_user(st.session_state["email"]):
            st.error("User already exists")
            time.sleep(1)
            st.session_state["verifying"] = False
            st.rerun()

    else:
        if st.button("Back to Login"):
            st.session_state["page"] = "login"
            st.rerun()

        with st.empty().container(border=True):
            st.title("Sign Up")

            # Email input with validation
            st.session_state["email"] = st.text_input("Email")
            if st.session_state["email"] and not is_valid_email(
                st.session_state["email"]
            ):
                st.error("Please enter a valid email address")

            # Password input
            st.session_state["password"] = st.text_input("Password", type="password")

            # Confirm password if required
            if confirmPass:
                confirm_password = st.text_input("Confirm Password", type="password")

            # Validate all required fields before proceeding
            if (
                st.session_state["email"]
                and st.session_state["password"]
                and (
                    not confirmPass
                    or (
                        confirmPass and st.session_state["password"] == confirm_password
                    )
                )
            ):

                if st.button("Register"):
                    st.session_state["verifying"] = True
                    if st.session_state["auth_db"].verify_duplicate_user(
                        st.session_state["email"]
                    ):
                        st.error("User already exists")
                    else:
                        st.session_state["auth_db"].insert_user_credentials(
                            st.session_state["email"], st.session_state["password"]
                        )

                    st.rerun()
            else:
                if confirmPass and st.session_state["password"] != confirm_password:
                    st.error("Passwords do not match")
                elif st.button("Register"):
                    st.error("Please fill in all required fields")
