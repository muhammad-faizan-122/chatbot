import streamlit as st
from utils.logger import log
from langchain_core.messages import HumanMessage, AIMessage
from utils.search_graph import GraphBuilder
from utils.db import Database


class ChatUI:
    """
    A class to encapsulate the Streamlit chat user interface,
    now with user authentication.
    """

    def __init__(self):
        """Initializes the ChatUI, database, and session state."""
        st.set_page_config(
            page_title="LangGraph Chatbot", page_icon="🤖", layout="centered"
        )
        self.db = Database()
        self.initialize_session_state()

    def initialize_session_state(self):
        """Initializes the session state variables if they don't exist."""
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "username" not in st.session_state:
            st.session_state.username = ""
        if "chatbot_graph" not in st.session_state:
            st.session_state.chatbot_graph = GraphBuilder.build_graph()

    def display_login_page(self):
        """Displays the login and sign-up forms."""
        st.title("Welcome to the LangGraph Chatbot")
        login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

        with login_tab:
            with st.form("login_form"):
                username = st.text_input("Username", key="login_username")
                password = st.text_input(
                    "Password", type="password", key="login_password"
                )
                submitted = st.form_submit_button("Login")
                if submitted:
                    if self.db.verify_user(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        # Load user's past conversations
                        st.session_state.messages = self.db.fetch_conversation_history(
                            username
                        )
                        st.rerun()
                    else:
                        st.error("Invalid username or password")

        with signup_tab:
            with st.form("signup_form"):
                new_username = st.text_input("Choose a Username", key="signup_username")
                new_password = st.text_input(
                    "Choose a Password", type="password", key="signup_password"
                )
                submitted = st.form_submit_button("Sign Up")
                if submitted:
                    if self.db.add_user(new_username, new_password):
                        st.success("Account created successfully! Please log in.")
                    else:
                        st.error("Username already exists.")

    def display_chat_page(self):
        """Displays the main chat interface for a logged-in user."""
        st.title("🤖 LangGraph Chatbot")

        # Logout button in the sidebar
        with st.sidebar:
            st.write(f"Welcome, {st.session_state.username}!")
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.session_state.messages = []
                st.rerun()

        # Display chat history
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Handle user input
        if prompt := st.chat_input("Type your message..."):
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            self.db.insert_conversation(st.session_state.username, "user", prompt)

            with st.chat_message("assistant"):
                response_text = st.write_stream(
                    self.get_assistant_response_stream(prompt)
                )
                st.session_state.messages.append(
                    {"role": "assistant", "content": response_text}
                )
                self.db.insert_conversation(
                    st.session_state.username, "assistant", response_text
                )

    def get_assistant_response_stream(self, user_prompt: str):
        """Gets the streaming response from the assistant."""
        log.info(f"User prompt from '{st.session_state.username}': {user_prompt}")
        try:
            for chunk in st.session_state.chatbot_graph.stream(
                {"messages": [HumanMessage(content=user_prompt)]},
                {
                    "configurable": {"thread_id": st.session_state.username}
                },  # Use username as thread_id
                stream_mode="values",
            ):
                if isinstance(chunk["messages"][-1], AIMessage):
                    yield chunk["messages"][-1].content
        except Exception as e:
            log.error(f"An error occurred while getting the assistant response: {e}")
            yield "Sorry, something went wrong. Please try again."

    def run(self):
        """Runs the main application, switching between login and chat pages."""
        if st.session_state.logged_in:
            self.display_chat_page()
        else:
            self.display_login_page()


if __name__ == "__main__":
    try:
        chat_ui = ChatUI()
        chat_ui.run()
    except Exception as e:
        log.critical(f"Failed to initialize and run the chatbot application: {e}")
