from src.llm.gemini.infer import Gemini
from src.llm.llamacpp.infer import LlamaGGUF


def get_llm_instant(llm_type: str):
    if llm_type == "gemini":
        llm = Gemini()

    elif llm_type == "llamacpp":
        llm = LlamaGGUF()

    else:
        raise ValueError("Select Correct llm type")

    return llm
