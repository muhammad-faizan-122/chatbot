from dotenv import load_dotenv


load_dotenv()


TEMPERATURE = 0.1
MAX_TOKENS = 100
SYSTEM_PROMPT = """You are a helpful bot assitant. \
Response user query concisely, friendly and professionally in the context \
of given previous conversation history (if given).
conversation: {conversation}"""
ENABLE_THINKING = 0
MODEL = "gemini-2.5-flash"
