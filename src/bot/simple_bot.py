from src.llm.llm_factory import get_llm_instant


class BOT:
    def __init__(self): ...


def get_bot_response(model_name="llamacpp"):

    llm = get_llm_instant()

    generator = llm.get_llm_generator("Hi")
    for chunk in generator:
        # print("chunk type: ", type(chunk))
        out = llm.extract_llm_response(chunk=chunk)
        if not out:
            continue
        print(out, end="")
