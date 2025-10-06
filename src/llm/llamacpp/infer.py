from llama_cpp import Llama
from src.common.logger import log
from src.common.utils import measure_time
from . import config
from src.llm.base import LLM


class LlamaGGUF(LLM):
    _instance = None
    llm = None

    # singleton pattern for load the LLM model only once
    def __new__(cls, *args, **kwargs):
        if not cls._instance and not cls.llm:
            cls._instance = super(LlamaGGUF, cls).__new__(cls)
            cls.llm = cls.load_llm()
        return cls._instance

    @classmethod
    def load_llm(cls):
        with measure_time("LLM model instance loading time", log):
            llm = Llama(
                model_path=config.MODEL_PATH,
                n_gpu_layers=config.GPU_LAYER,
                seed=config.SEED,
                n_ctx=config.CTX_LEN,
                verbose=config.VERBOSE,
            )
        return llm

    def add_context(self, history: list) -> list[dict]:
        messages = []
        conversation = self.format_conversation(history)
        messages.append(
            {
                "role": "system",
                "content": config.SYSTEM_PROMPT.format(conversation=conversation),
            }
        )
        return messages

    def get_llm_generator(
        self, query: str, chat_history: list = [], context_type="filter"
    ):
        managed_context = self.manage_context(chat_history, type=context_type)
        log.debug(f"Context after context_manager: {managed_context}")
        messages = self.add_context(managed_context)
        user_query = {"role": "user", "content": query}
        messages.append(user_query)
        log.debug(f"LLM Prompt: {messages}")
        try:
            with measure_time("instantiate generator time: ", log):
                generator = self.llm.create_chat_completion(
                    max_tokens=config.MAX_TOKENS,
                    temperature=config.TEMPERATURE,
                    stream=config.ALLOW_STREAM,
                    messages=messages,
                )
                return generator

        except Exception as e:
            log.error(f"Failed to instantiate the LLM generator.\n{e}")
            raise

    def extract_llm_response(self, chunk):
        try:
            llm_response = chunk["choices"][0]["delta"].get("content", "")
            return llm_response
        except Exception as e:
            log.error(f"Failed to extract the text from streaming chunk.\n{e}")
            return ""

    def infer_llm(self, messages: list[dict]):
        log.debug(f"LLM Prompt: {messages}")
        try:
            with measure_time("instantiate generator time: ", log):
                response = self.llm.create_chat_completion(
                    max_tokens=config.MAX_TOKENS,
                    temperature=config.TEMPERATURE,
                    stream=config.ALLOW_STREAM,
                    messages=messages,
                )
                content = self.extract_llm_response(response)
                return content

        except Exception as e:
            log.error(f"Failed to instantiate the LLM generator.\n{e}")
            raise

    def get_bot_response(self, messages: list):
        system_instruction = """You are a helpful assitant. Response very concisely, friendly and professionally in the context of given conversation."""
        messages = [{"role": "system", "content": system_instruction}] + messages
        response = self.infer_llm(messages)
        return response

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
