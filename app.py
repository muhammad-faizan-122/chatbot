import streamlit as st
from utils.logger import log
from langchain_core.messages import HumanMessage, AIMessage
from utils.search_graph import GraphBuilder
from utils.db import Database
import uuid


class ChatUI:
    """
    A class to encapsulate the Streamlit chat user interface.

    This class follows the Single Responsibility Principle (SRP) by focusing
    solely on the presentation logic of the chat application.
    """

    def __init__(self):
        """
        Initializes the ChatUI with a compiled LangGraph.

        Args:
            graph: A compiled LangGraph instance.
        """
        st.set_page_config(
            page_title="LangGraph Chatbot",
            page_icon="🤖",
            layout="centered",
        )
        st.title("🤖 LangGraph Chatbot")
        self.initialize_session_state()
        self.db = Database()
        log.info("ChatUI initialized successfully.")

    def get_uuid(self):
        """Generates a unique identifier for the session."""
        return str(uuid.uuid4())

    def initialize_session_state(self):
        """Initializes the session state if it doesn't exist."""
        if "messages" not in st.session_state:
            st.session_state.messages = []
            st.session_state.chatbot_graph = GraphBuilder.build_graph()
            st.session_state.user_id = self.get_uuid()
            log.debug("Session state initialized for a new user.")

    def display_chat_history(self):
        """Displays the chat history from the session state."""
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    def get_assistant_response_stream(self, user_prompt: str):
        """
        Gets the streaming response from the assistant.

        Args:
            user_prompt: The user's input message.

        Yields:
            The content of the AIMessage chunks.
        """
        log.info(f"User prompt: {user_prompt}")
        try:
            for chunk in st.session_state.chatbot_graph.stream(
                {"messages": [HumanMessage(content=user_prompt)]},
                {"configurable": {"thread_id": "1"}},
                stream_mode="values",
            ):
                if isinstance(chunk["messages"][-1], AIMessage):
                    response_content = chunk["messages"][-1].content
                    log.debug(f"Assistant response chunk: {response_content}")
                    yield response_content
        except Exception as e:
            log.error(f"An error occurred while getting the assistant response: {e}")
            yield "Sorry, something went wrong. Please try again."

    def handle_user_input(self):
        """Handles the user input and displays the assistant's response."""
        if prompt := st.chat_input("Type your message..."):
            if not prompt.strip():
                log.warning("User submitted an empty prompt.")
                return

            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            self.db.insert_conversation(st.session_state.user_id, "user", prompt)
            with st.chat_message("assistant"):
                response_text = st.write_stream(
                    self.get_assistant_response_stream(prompt)
                )
                st.session_state.messages.append(
                    {"role": "assistant", "content": response_text}
                )
                self.db.insert_conversation(
                    st.session_state.user_id, "assistant", response_text
                )
            log.info("Successfully displayed assistant response.")

    def run(self):
        """Runs the main chat application loop."""
        self.display_chat_history()
        self.handle_user_input()


if __name__ == "__main__":
    try:
        chat_ui = ChatUI()
        chat_ui.run()
    except Exception as e:
        log.critical(f"Failed to initialize and run the chatbot application: {e}")
