from abc import ABC, abstractmethod


class LLM(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_llm_generator(self, query: str):
        return

    @abstractmethod
    def extract_llm_response(chunk):
        return

    def format_conversation(self, history: list) -> str:
        """Prepare conversation for LLM history"""
        conversation = ""
        for message in history:
            conversation += f"user: {message['user']}\nassistant:{message['AI']}" + "\n"
        return conversation

    def get_conversation_text(messages: list):
        if not len(messages):
            return ""
        text = ""
        for message in messages:
            if "role" in message or "content" in message:
                text += f"{message['role']}: {message['content']}" + "\n"

            else:
                # TODO: ADD WARNING LOG IF MISSING ROLE OR CONTENT IN MESSAGE DICT
                ...
        return text

    def get_summary_prompt(self, messages: list):
        """Prepare the summary prompt in chat format prompt"""
        system_instruction = f"""You are expert in summarizing conversational dialogue. Given conversation return concise summary only."""
        conversation = self.get_conversation_text(messages)
        summary_prompt = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": conversation},
        ]
        return summary_prompt

    def filter_messages(self, messages, max_turns=7):
        """single turn means if `Person: caption`"""
        total_messages = len(messages)
        # find the starting index conversation, -1 is due to index start from 0
        start_conversation = max(0, total_messages - max_turns - 1)
        # skip the latest user message
        return messages[start_conversation:-1]

    def trim_messages(self, messages: list):
        NotImplemented
