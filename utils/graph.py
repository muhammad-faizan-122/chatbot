from .logger import log
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from .states import State
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables from .env file
load_dotenv(override=True)


class ChatbotNode:
    """
    Represents the core logic of the chatbot.
    """

    def __init__(self, chat_model):
        """
        Initializes the ChatbotNode with a chat model.
        """
        self.chat_model = chat_model
        log.info("ChatbotNode initialized.")

    def execute(self, state: State) -> dict:
        """
        Executes the chatbot logic.
        """
        log.debug(f"Executing ChatbotNode with state: {state}")
        try:
            response = {"messages": [self.chat_model.invoke(state["messages"])]}
            log.debug(f"ChatbotNode response: {response}")
            return response
        except Exception as e:
            log.error(f"Error in ChatbotNode execution: {e}")
            raise


class GraphBuilder:
    """
    Builds the LangGraph for the chatbot.
    """

    def __init__(self, model_name: str = "google_genai:gemini-1.5-flash"):
        """
        Initializes the GraphBuilder.
        """
        self.model_name = model_name
        log.info(f"GraphBuilder initialized with model: {self.model_name}")

    def build_graph(self):
        """
        Builds and compiles the LangGraph.
        """
        chat_model = init_chat_model(self.model_name)
        chatbot_node = ChatbotNode(chat_model=chat_model)
        log.info("Chat model and ChatbotNode created.")

        memory = MemorySaver()
        bot_graph = StateGraph(State)

        bot_graph.add_node("chatbot", chatbot_node.execute)
        bot_graph.add_edge(START, "chatbot")
        bot_graph.add_edge("chatbot", END)
        log.info("Graph nodes and edges defined.")

        compiled_graph = bot_graph.compile(checkpointer=memory)
        log.info("Graph compiled successfully with memory saver.")
        return compiled_graph
