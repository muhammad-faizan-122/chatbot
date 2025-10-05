import os
import sys

sys.path.append(os.getcwd())
from src.llm.llm_factory import get_llm_instant


SYSTEM_PROMPT = "You are a helpful bot assitant. Response very concisely, friendly and professionally in the context of given previous conversation history."


chat_history = [
    {"role": "user", "content": "I am Faizan."},
    {"role": "assistant", "content": "Hi Faizan, how are you doing?"},
    {"role": "user", "content": "Good"},
    {"role": "assistant", "content": "Great!"},
]

query = "what is my name?"

llm = get_llm_instant("llamacpp")
tokens = llm.get_llm_generator(query=query, chat_history=chat_history)
response = []
for token in tokens:
    content = llm.extract_llm_response(token)
    print(content, end="")
    response.append(content)
