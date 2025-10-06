import os


CTX_LEN = 2048
GPU_LAYER = -1  # -1 FOR CPU
MODEL_PATH = "./model/Llama-3.2-1B-Instruct-IQ3_M.gguf"
TEMPERATURE = 0.1
MAX_TOKENS = 300
ALLOW_STREAM = True
SEED = 1337
VERBOSE = False
SYSTEM_PROMPT = """You are a helpful bot assitant. \
Response user query concisely, friendly and professionally in the context \
of given previous conversation history (if given).
conversation: {conversation}"""
