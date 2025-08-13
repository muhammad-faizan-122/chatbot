import streamlit as st
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv


# Load environment variables
load_dotenv(override=True)


# Define the state for LangGraph
class State(TypedDict):
    messages: Annotated[list, add_messages]


# Initialize LLM
llm = init_chat_model("google_genai:gemini-2.0-flash")


# Chatbot node function
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

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
