from datetime import datetime
from pymongo.collection import Collection
from typing import Optional
from .repository import MongoRepository
from .utils.security import hash_password, is_password_correct
from src.common.logger import log


class AuthenticatorDb:
    def __init__(self, collection: Collection, repo: MongoRepository):
        self.collection = collection
        self.repo = repo

    def verify_duplicate_user(self, user_name: str) -> bool:
        return self.collection.find_one({"userName": user_name}) is not None

    def insert_user_credentials(self, user_name: str, password: str) -> str:
        user_doc = {
            "userName": user_name,
            "password": hash_password(password),
            "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        return self.repo.insert_one(user_doc, self.collection)

    def authenticate_user(self, user_name: str, password: str) -> Optional[str]:
        matched_user = self.repo.fetch_one({"userName": user_name}, self.collection)
        if not matched_user:
            log.error("User not found")
            return "no_user"

        if not is_password_correct(password, matched_user["password"]):
            log.error("Incorrect password")
            return "incorrect_password"

        return str(matched_user["_id"])
