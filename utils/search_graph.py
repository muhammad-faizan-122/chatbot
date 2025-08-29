from .logger import log
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from .states import State
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from .commons import save_json_file
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables from .env file
load_dotenv(override=True)


class RouterQuery(BaseModel):
    """Router for selecting the next node."""

    route: str = Field(
        description="Given the user query, choose 'web_search' if it requires real-time, up-to-date information or 'chatbot' for general conversation.",
        enum=["web_search", "chatbot"],
    )


class ChatbotNode:
    """
    Generates a response based on the conversation history and provided documents.
    """

    def __init__(self, chat_model):
        self.chat_model = chat_model
        log.info("ChatbotNode initialized.")

    def execute(self, state: State) -> dict:
        """
        Executes the chatbot logic. If documents are present, they are used as context.
        """
        log.debug(f"Executing ChatbotNode with state: {state}")
        messages = state["messages"]
        documents = state.get("documents")  # Use .get for safety
        log.debug(f"Documents received: {documents}")

        if documents:
            # If documents are available, augment the prompt with them
            context = "\n".join(
                [doc.get("content", "") for doc in documents.get("results", [])]
            )
            log.debug(f"Context for ChatbotNode: {context}")
            prompt_template = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "You are a helpful assistant. Answer the user's question based on the following context very concisely:\n\n{context}",
                    ),
                    ("user", "{user_query}"),
                ]
            )
            prompt = prompt_template.invoke(
                {"context": context, "user_query": messages[-1].content}
            )
            messages = prompt.to_messages()
            log.debug(f"LLM prompt messages with context: {messages}")
        try:
            response = self.chat_model.invoke(messages)
            log.debug(f"ChatbotNode response: {response}")
            return {"messages": [response], "documents": documents}

        except Exception as e:
            log.error(f"Error in ChatbotNode execution: {e}")
            raise


class WebSearchNode:
    """
    Performs a web search using the Tavily API.
    """

    def __init__(self):
        self.search_tool = TavilySearch(max_results=2)
        log.info("WebSearchNode initialized with Tavily Search.")

    def execute(self, state: State) -> dict:
        """
        Executes the web search based on the latest user message.
        """
        log.debug("Executing WebSearchNode.")
        try:
            last_message = state["messages"][-1]
            query = last_message.content
            log.info(f"Performing web search for query: {query}")
            retrieved_docs = self.search_tool.invoke({"query": query})
            log.debug(f"Web search results: {retrieved_docs}")
            save_json_file(retrieved_docs, fname="web_search_results")
            return {"documents": retrieved_docs}
        except Exception as e:
            log.error(f"Error in WebSearchNode execution: {e}")
            raise


class GraphBuilder:
    """
    Builds the LangGraph for the chatbot with web search capability.
    """

    @staticmethod
    def router_function(state: State, structured_llm):
        """
        Determines the next step in the graph.
        """
        log.info("Executing router.")
        query = state["messages"][-1].content
        try:
            router_result = structured_llm.invoke(query)
            log.debug(f"Router decision: {router_result.route}")
            return router_result.route
        except Exception as e:
            log.error(f"Error in router execution: {e}")
            # Default to chatbot on error
            return "chatbot"

    @staticmethod
    def build_graph(model_name: str = "google_genai:gemini-1.5-flash"):
        """
        Builds and compiles the LangGraph.
        """
        chat_model = init_chat_model(model_name)

        # LLM with function calling for the router
        structured_llm = chat_model.with_structured_output(RouterQuery)

        # Initialize nodes
        chatbot_node = ChatbotNode(chat_model=chat_model)
        web_search_node = WebSearchNode()
        log.info("Chat model and all nodes created.")

        bot_graph = StateGraph(State)

        # Add nodes to the graph
        bot_graph.add_node("chatbot", chatbot_node.execute)
        bot_graph.add_node("web_search", web_search_node.execute)

        # The entry point is now a conditional router
        bot_graph.add_conditional_edges(
            START,
            lambda state: GraphBuilder.router_function(state, structured_llm),
            {
                "web_search": "web_search",
                "chatbot": "chatbot",
            },
        )

        # Define the flow after web search
        bot_graph.add_edge("web_search", "chatbot")
        bot_graph.add_edge("chatbot", END)
        log.info("Graph nodes and edges defined.")

        memory = MemorySaver()
        # Compile the graph with a memory saver
        compiled_graph = bot_graph.compile(checkpointer=memory)
        log.info("Graph compiled successfully.")
        return compiled_graph
