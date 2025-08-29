import streamlit as st
from graph import get_graph


graph = get_graph()

# Streamlit App
st.set_page_config(page_title="LangGraph Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 LangGraph Chatbot")

# Store conversation in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Get assistant response from LangGraph
    with st.chat_message("assistant"):
        placeholder = st.empty()
        response_text = ""
        for event in graph.stream({"messages": st.session_state.messages}):
            for value in event.values():
                chunk = value["messages"][-1].content
                response_text = chunk  # overwrite with latest
                placeholder.markdown(response_text)
        st.session_state.messages.append(
            {"role": "assistant", "content": response_text}
        )
