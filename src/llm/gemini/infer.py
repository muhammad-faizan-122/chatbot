from src.llm.base import LLM
from google import genai
from google.genai import types
from . import config
from src.common.logger import log
from src.common.utils import measure_time


class Gemini(LLM):
    _instance = None
    llm_client = None

    # singleton pattern for load the LLM model only once
    def __new__(cls, *args, **kwargs):
        if not cls._instance and not cls.llm_client:
            cls._instance = super(Gemini, cls).__new__(cls)
            cls.llm_client = cls.load_llm()
        return cls._instance

    @classmethod
    def load_llm(cls):
        with measure_time("LLM model instance loading time", log):
            client = genai.Client()
        return client

    def __init__(self):
        self.messages = [
            {"role": "system", "content": config.SYSTEM_PROMPT},
            {"role": "user", "content": ""},
        ]

    def get_llm_generator(self, query: str, chat_history: list = []):
        log.debug(f"LLM Prompt: {self.messages}")
        try:
            with measure_time("instantiate generator time: ", log):
                generator = self.llm_client.models.generate_content_stream(
                    model=config.MODEL,
                    contents=[query],
                    config=types.GenerateContentConfig(
                        thinking_config=types.ThinkingConfig(
                            thinking_budget=config.ENABLE_THINKING
                        ),
                        max_output_tokens=config.MAX_TOKENS,
                        system_instruction=config.SYSTEM_PROMPT,
                        temperature=config.TEMPERATURE,
                    ),
                )
                return generator

        except Exception as e:
            log.error(f"Failed to instantiate the LLM generator.\n{e}")
            raise

    def extract_llm_response(self, chunk):
        try:
            llm_response = chunk.text
            return llm_response
        except Exception as e:
            log.error(f"Failed to extract the text from streaming chunk.\n{e}")
            return ""

    def infer_llm(self, prompt: str):
        log.debug(f"LLM Prompt: {self.messages}")
        try:
            system_instruction = """You are a helpful assitant. Response very concisely, friendly and professionally in the context of given conversation."""
            with measure_time("instantiate generator time: ", log):
                response = self.llm_client.models.generate_content(
                    model=config.MODEL,
                    contents=[prompt],
                    config=types.GenerateContentConfig(
                        thinking_config=types.ThinkingConfig(
                            thinking_budget=config.ENABLE_THINKING
                        ),
                        max_output_tokens=200,
                        system_instruction=system_instruction,
                        temperature=config.TEMPERATURE,
                    ),
                )
                return response.text

        except Exception as e:
            log.error(f"Failed to instantiate the LLM generator.\n{e}")
            raise

    def summarize_messages(self, messages: list):
        """summarize the conversation messages"""
        messages_prompt = self.get_summary_prompt(messages)
        summary = self.infer_llm(messages_prompt)
        return summary

    def manage_context(
        self,
        messages,
        type="filter",
        types=["filter", "summarize", "trim"],
    ):

        if type not in types:
            raise ValueError(
                f"Select appropriate context mananger type out these only: {types}"
            )
        if type == "filter":
            return self.filter_messages(messages=messages)
        elif type == "summarize":
            return self.summarize_messages(messages=messages)
        elif type == "trim":
            return self.trim_messages(messages=messages)
