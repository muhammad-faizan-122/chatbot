import streamlit as st


def login_page(guest_mode=False):
    with st.empty().container(border=True):
        col1, _, col2 = st.columns([10, 1, 10])

        with col1:
            st.write("")
            st.write("")
            st.write("")
            st.image("data/demo.png")

        with col2:
            st.title("Login")

            email = st.text_input("E-mail")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if not (email and password):
                    st.error("Please provide email and password")

                elif email and password:
                    user_id = st.session_state["auth_db"].authenticate_user(
                        email,
                        password,
                    )
                    if user_id == "no_user":
                        st.error("E-mail not exist, please sign up.")

                    elif user_id == "incorrect_password":
                        st.error("Entered incorrect password!")
                    else:
                        st.session_state["authenticated"] = True
                        st.session_state["page"] = "app"
                        st.session_state["user_id"] = user_id
                        st.rerun()
                else:
                    st.error("Invalid login credentials")

            if st.button("Sign Up"):
                st.session_state["page"] = "signup"
                st.rerun()

            if guest_mode:
                if st.button("Continue as Guest"):
                    st.session_state["guest_mode"] = True
                    st.session_state["authenticated"] = True
                    st.session_state["page"] = "app"
                    st.rerun()
