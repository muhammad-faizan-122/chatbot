import os
import sys

sys.path.append(os.getcwd())
from src.db.mongodb import MongoDB
from datetime import datetime


# db = MongoDB(db_name="bot", collection_name="chats")

# doc = {
#     "user_id": "1212",
#     "conversation_id": "2121",
#     "user": "Hi",
#     "AI": "how can I assist you?",
# }
# id = db.insert_one(doc)
# print(id)


# docs = db.fetch_all()
# print(docs)


# db.fetch_one(
#     {
#         "user_id": "1212",
#         "conversation_id": "2121",
#         "user": "Hi",
#         "AI": "how can I assist you?",
#     }
# )

# history = db.fetch_history(user_id="1212", conversation_id="2121")
# print(f"history: {history}")

# db.delete_many(
#     {
#         "user_id": "1212",
#         "conversation_id": "2121",
#         "user": "Hi",
#         "AI": "how can I assist you?",
#     }
# )

# db = MongoDB(db_name="bot", collection_name="chats")


# docs = [
#     {
#         "user_id": "1212",
#         "conversation_id": "2121",
#         "user": "Hi",
#         "AI": "how can I assist you?",
#         "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#     },
#     {
#         "user_id": "1212",
#         "conversation_id": "2121",
#         "user": "Hi",
#         "AI": "how can I assist you?",
#         "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#     },
#     {
#         "user_id": "1212",
#         "conversation_id": "1234",
#         "user": "Hi",
#         "AI": "how can I assist you?",
#         "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#     },
#     {
#         "user_id": "1212",
#         "conversation_id": "1234",
#         "user": "Hi",
#         "AI": "how can I assist you?",
#         "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#     },
# ]

# db.insert_many(docs)


# db.delete_many({"conversation_id": "2121"})
# print(f"db: ", db)
