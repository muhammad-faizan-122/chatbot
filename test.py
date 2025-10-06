history = [
    {
        "_id": ("68e35a7e3fa739634111b9e2"),
        "user_id": "68e350a874fe97a60a8a29de",
        "conversation_id": "6b06e176-f450-4a83-987c-3da262366c28",
        "user": "Hi",
        "AI": "Hello again! How can I assist you today?",
        "timestamp": "2025-10-06 10:58:22",
    },
    {
        "_id": ("68e35a853fa739634111b9e3"),
        "user_id": "68e350a874fe97a60a8a29de",
        "conversation_id": "6b06e176-f450-4a83-987c-3da262366c28",
        "user": "how are you?",
        "AI": "I'm doing well, thank you for asking! It's great to see you again. How about you? How's your day going so far?",
        "timestamp": "2025-10-06 10:58:29",
    },
    {
        "_id": ("68e35a953fa739634111b9e4"),
        "user_id": "68e350a874fe97a60a8a29de",
        "conversation_id": "6b06e176-f450-4a83-987c-3da262366c28",
        "user": "what is your purpose?",
        "AI": "I'm an AI designed to assist and communicate with users in a helpful and informative way. My purpose is to provide accurate and relevant information, answer questions, and engage in conversation to the best of my abilities. I'm a large language model, trained on a vast amount of text data, which enables me to generate responses that are tailored to specific topics and contexts. My goal is to provide assistance, answer questions, and help users like you with any queries or concerns you may have.",
        "timestamp": "2025-10-06 10:58:45",
    },
    {
        "_id": ("68e35aab3fa739634111b9e5"),
        "user_id": "68e350a874fe97a60a8a29de",
        "conversation_id": "6b06e176-f450-4a83-987c-3da262366c28",
        "user": "how you predict next word?",
        "AI": "I use various natural language processing (NLP) techniques to predict the next word in a sentence. Here's a simplified overview of my prediction mechanism:\n\n1. **Tokenization**: I break down the input sentence into individual words or tokens.\n2. **Part-of-speech tagging**: I identify the part of speech (e.g., noun, verb, adjective, etc.) for each token.\n3. **Contextual analysis**: I analyze the context of the sentence, including the surrounding words, to",
        "timestamp": "2025-10-06 10:59:07",
    },
    {
        "_id": ("68e35aed3fa739634111b9e6"),
        "user_id": "68e350a874fe97a60a8a29de",
        "conversation_id": "6b06e176-f450-4a83-987c-3da262366c28",
        "user": "what are NLP",
        "AI": "**Natural Language Processing (NLP)** is a subfield of artificial intelligence (AI) that deals with the interaction between computers and human language. It's a way to enable computers to understand, process, and generate human language.\n\n**Key aspects of NLP:**\n\n1. **Text analysis**: NLP helps computers to understand the meaning of text, including grammar, syntax, and semantics.\n2. **Language modeling**: NLP enables computers to learn patterns and relationships in language, allowing them to",
        "timestamp": "2025-10-06 11:00:13",
    },
    {
        "_id": ("68e35b123fa739634111b9e7"),
        "user_id": "68e350a874fe97a60a8a29de",
        "conversation_id": "6b06e176-f450-4a83-987c-3da262366c28",
        "user": "okay",
        "AI": "I can see that you're not interested in continuing the conversation about NLP. Would you like to discuss something else?",
        "timestamp": "2025-10-06 11:00:50",
    },
    {
        "_id": ("68e35b1a3fa739634111b9e8"),
        "user_id": "68e350a874fe97a60a8a29de",
        "conversation_id": "6b06e176-f450-4a83-987c-3da262366c28",
        "user": "no",
        "AI": "It was nice chatting with you. If you ever need assistance or have questions, feel free to reach out. Have a great day!",
        "timestamp": "2025-10-06 11:00:58",
    },
    {
        "_id": ("68e35ce43fa739634111b9e9"),
        "user_id": "68e350a874fe97a60a8a29de",
        "conversation_id": "6b06e176-f450-4a83-987c-3da262366c28",
        "user": "do you know about Imran khan?",
        "AI": "You're likely referring to Imran Khan, the former Pakistani politician and cricketer. He's a well-known figure in Pakistan, and his name has been in the news recently due to various controversies.\n\nIs there something specific you'd like to know about Imran Khan or his recent activities?",
        "timestamp": "2025-10-06 11:08:36",
    },
]

from src.llm.llm_factory import get_llm_instant


llm = get_llm_instant("llamacpp")

llm.filter_messages(history)
