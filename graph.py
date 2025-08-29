from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from states import State
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)


# Initialize LLM
llm = init_chat_model("google_genai:gemini-2.0-flash")


# Chatbot node function
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


def build_graph():
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)
    return graph_builder


def get_graph():
    builder = build_graph()
    graph = builder.compile()
    return graph
