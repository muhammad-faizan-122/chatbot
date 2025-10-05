import sys
import os

sys.path.append(os.getcwd())


from src.llm.llamacpp.infer import LlamaGGUF
from src.llm.gemini.infer import Gemini


def get_llm_instant(llm_name: str):
    if llm_name == "gemini":
        llm = Gemini()

    elif llm_name == "llamacpp":
        llm = LlamaGGUF()

    else:
        raise ValueError("Select Correct llm type")
    return llm


llm = get_llm_instant(llm_name="llamacpp")
generator = llm.get_llm_generator("Hi")
for chunk in generator:
    # print("chunk type: ", type(chunk))
    out = llm.extract_llm_response(chunk=chunk)
    if not out:
        continue
    print(out, end="")
