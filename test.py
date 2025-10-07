from src.db.mongo.connection import get_database
from src.db.mongo.repository import MongoRepository
from src.db.mongo.chat import ChatDb
from src.db.mongo.auth import AuthenticatorDb


# Setup
db = get_database()
repo = MongoRepository()

# Collections
chat_collection = db["chat"]
auth_collection = db["users"]

# Services
chat_service = ChatDb(chat_collection, repo)
auth_service = AuthenticatorDb(auth_collection, repo)

# Example usage
chat_service.save_chat_history(
    {"user_id": "123", "conversation_id": "abc", "text": "Hello"}
)
user_id = auth_service.insert_user_credentials("faizan", "securepassword")
