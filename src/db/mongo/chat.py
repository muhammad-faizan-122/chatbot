from pymongo.collection import Collection
from .repository import MongoRepository
from src.common.logger import log


class ChatDb:
    def __init__(self, collection: Collection, repo: MongoRepository):
        self.collection = collection
        self.repo = repo

    def save_chat_history(self, chat_history: dict):
        user_id = self.repo.insert_one(chat_history, self.collection)
        log.info(f"Chat history saved for user id: {user_id}")
        return user_id

    def fetch_conversation_history(self, user_id, conversation_id):
        return list(
            self.collection.find(
                {"user_id": user_id, "conversation_id": conversation_id}
            )
        )
