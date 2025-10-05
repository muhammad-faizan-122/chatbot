import streamlit as st
from src.pages.utils.session_states import reset_session
from src.llm.llm_factory import get_llm_instant
from src.db.mongodb import MongoDB
from datetime import datetime
import uuid


def response_generator(prompt, chat_history):
    response = st.session_state["llm"].get_llm_generator(prompt, chat_history)
    for chunk in response:
        token = st.session_state["llm"].extract_llm_response(chunk)
        yield "" if not token else token + ""


def app_page():

    with st.sidebar:
        if st.session_state["guest_mode"]:
            st.subheader("Guest Mode")

            if not st.session_state["user_id"]:
                st.session_state["user_id"] = str(uuid.uuid4())
                print("guest mode user_id", st.session_state["user_id"])

            if st.button("Login"):
                print("Deleting all the Guess conversation.")
                # No need to persist guess model conversation.
                st.session_state["chat_db"].delete_many(
                    {
                        "user_id": st.session_state["user_id"],
                        "conversation_id": st.session_state["conversation_id"],
                    }
                )
                reset_session()
                st.rerun()

        else:
            if st.button("Logout"):
                reset_session()
                st.rerun()

    st.title("Chatbot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        st.session_state["llm"] = get_llm_instant(llm_type="llamacpp")
        st.session_state["chat_db"] = MongoDB(db_name="bot", collection_name="chats")
        st.session_state["guest_history"] = []

    # Display chat messages from history on app rerun
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask anything"):

        # Add user message to chat history
        st.session_state["messages"].append({"role": "user", "content": prompt})

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        if st.session_state["guest_mode"]:
            chat_history = st.session_state["guest_history"]
        else:
            chat_history = st.session_state["chat_db"].fetch_conversation_history(
                st.session_state["user_id"],
                st.session_state["conversation_id"],
            )

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(prompt, chat_history))

        # Add assistant response to chat history
        st.session_state["messages"].append({"role": "assistant", "content": response})

        chat_info = {
            "user_id": st.session_state["user_id"],
            "conversation_id": st.session_state["conversation_id"],
            "user": prompt,
            "AI": "".join(response),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        # Maintain temp memory for guest mode without saving into Database
        if st.session_state["guest_mode"]:
            st.session_state["guest_history"].append(chat_info)
        else:
            st.session_state["chat_db"].insert_one(chat_info)
