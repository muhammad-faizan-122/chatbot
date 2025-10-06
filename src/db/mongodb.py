from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from typing import List, Optional
from src.common.logger import log
from datetime import datetime
import bcrypt
import streamlit as st


class MongoDB:
    _instance = None
    _client: Optional[MongoClient] = None
    _db = None
    _collection = None

    def __new__(
        cls,
        db_name,
        collection_name,
        host: str = "localhost",
        port: int = 27017,
    ):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                cls._client = MongoClient(host=host, port=port)
                cls._db = cls._client[db_name]
                cls._collection = cls._db[collection_name]
                log.info("MongoDB connected successfully.")
            except PyMongoError as e:
                log.error(f"Connection to MongoDB failed: {e}")
                raise

        else:
            log.info("client collection is already created...")
        return cls._instance

    def get_collection(self, collection_name: str) -> Collection:
        try:
            return self._db[collection_name]
        except Exception as e:
            log.error(f"Failed to access collection: {e}")
            raise

    def insert_one(self, doc: dict) -> str:
        try:
            if not isinstance(doc, dict):
                raise ValueError("Document must be a dictionary")
            result = self._collection.insert_one(doc)
            return str(result.inserted_id)
        except PyMongoError as e:
            log.error(f"Insert failed: {e}")
            raise

    def insert_many(self, docs: list[dict]):
        try:
            if not isinstance(docs, list):
                raise ValueError("Documents must be a list of dictionaries")
            result = self._collection.insert_many(docs)
            return bool(result.inserted_ids)
        except PyMongoError as e:
            log.error(f"Insert many failed: {e}")
            return False

    def fetch_one(self, filter_query: dict) -> Optional[dict]:
        if not isinstance(filter_query, dict):
            raise ValueError("Filter query must be a dictionary")
        matched_doc = self._collection.find_one(filter_query)
        return matched_doc if matched_doc else False

    def fetch_conversation_history(self, user_id, conversation_id):
        history = []
        for doc in self._collection.find():
            if (
                doc.get("user_id") == user_id
                and doc.get("conversation_id") == conversation_id
            ):
                history.append(doc)
        return history

    def fetch_all(self) -> List[dict]:
        try:
            return [doc for doc in self._collection.find()]
        except PyMongoError as e:
            log.error(f"Fetch all failed: {e}")
            return []

    def update_one(
        self,
        filter_query: dict,
        update_data: dict,
        upsert: bool = True,
    ) -> bool:
        try:
            result = self._collection.update_one(
                filter_query, {"$set": update_data}, upsert=upsert
            )
            return result.acknowledged and result.modified_count > 0
        except PyMongoError as e:
            log.error(f"Update one failed: {e}")
            return False

    def update_many(
        self,
        filter_query: dict,
        update_data: dict,
        upsert: bool = True,
    ) -> bool:
        try:
            result = self._collection.update_many(
                filter_query, {"$set": update_data}, upsert=upsert
            )
            log.debug(f"Total updated: {result.modified_count}")
            return result.acknowledged and result.modified_count > 0
        except PyMongoError as e:
            log.error(f"Update many failed: {e}")
            return False

    def delete_one(self, filter_query: dict) -> bool:
        try:
            result = self._collection.delete_one(filter_query)
            log.info(f"Deleted document: {result.deleted_count}")
            return result.acknowledged and result.deleted_count > 0
        except PyMongoError as e:
            log.error(f"Delete one failed: {e}")
            return False

    def delete_many(self, filter_query: dict = {}) -> bool:
        """On defualt arg, it will delete all argument"""
        try:
            result = self._collection.delete_many(filter_query)
            log.info(f"Deleted all documents: {result.deleted_count}")
            return result.acknowledged and result.deleted_count > 0
        except PyMongoError as e:
            log.error(f"Delete many failed: {e}")
            return False

    def close_connection(self):
        self._client.close()

    def __repr__(self):
        return "MongoDB"


class Authenticator(MongoDB):
    def __init__(self, db_name, collection_name):
        self._db = self._client[db_name]
        self._collection = self._db[collection_name]

    def hash_password(self, password: str) -> bytes:
        password_bytes = password.encode(encoding="utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password.decode(encoding="utf-8")

    def verify_duplicate_user(self, user_name: str) -> bool:
        """
        Return None if user_name not exist in users collection
        """

        if isinstance(user_name, str):
            query = {"userName": user_name}

        return False if not self._collection.find_one(query) else True

    def insert_user_credentials(self, user_name, password):
        """For sign Up inserting user's credentials to DB"""
        user_creds = {
            "userName": user_name,
            "password": self.hash_password(password),
            "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        user_id = self.insert_one(user_creds)
        return user_id

    def authenticate_user(self, user_name: str, password: str) -> Optional[str]:
        """
        Authenticates a user by checking username and password.

        Returns:
            if User info exist return matched user ID, otherwise None
        """
        matched_user = self.fetch_one({"userName": user_name})
        if not matched_user:
            st.error("E-mail not exist, please sign up.")
            return None

        password_hash = matched_user["password"]
        is_password_correct = bcrypt.checkpw(password.encode(), password_hash.encode())
        if not is_password_correct:
            st.error(f"Entered incorrect password!")
            return None

        return str(matched_user["_id"])
