from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from typing import List, Optional
from src.common.logger import log
from datetime import datetime
import bcrypt
import streamlit as st
from . import config
from abc import ABC


class MongoDb(ABC):
    _db_instance = None
    _client: Optional[MongoClient] = None
    _db = None

    def __new__(cls):
        if cls._db_instance is None:
            cls._db_instance = super().__new__(cls)
            try:
                cls._client = MongoClient(host=config.host, port=config.port)
                cls._db = cls._client[config.db_name]
                log.info("MongoDB connected successfully.")
            except PyMongoError as e:
                log.error(f"Connection to MongoDB failed: {e}")
                raise
        else:
            log.info("client collection is already created...")
        return cls._db_instance

    def get_collection(self, collection_name: str) -> Collection:
        try:
            return self._db[collection_name]
        except Exception as e:
            log.error(f"Failed to access collection: {e}")
            raise

    def insert_one(self, doc: dict, collection) -> str:
        try:
            if not isinstance(doc, dict):
                raise ValueError("Document must be a dictionary")
            result = collection.insert_one(doc)
            return str(result.inserted_id)
        except PyMongoError as e:
            log.error(f"Insert failed: {e}")
            raise

    def insert_many(self, docs: list[dict], collection):
        try:
            if not isinstance(docs, list):
                raise ValueError("Documents must be a list of dictionaries")
            result = collection.insert_many(docs)
            return bool(result.inserted_ids)
        except PyMongoError as e:
            log.error(f"Insert many failed: {e}")
            return False

    def fetch_one(self, filter_query: dict, collection) -> Optional[dict]:
        if not isinstance(filter_query, dict):
            raise ValueError("Filter query must be a dictionary")
        matched_doc = collection.find_one(filter_query)
        return matched_doc if matched_doc else False

    def fetch_all(self, collection) -> List[dict]:
        try:
            return [doc for doc in collection.find()]
        except PyMongoError as e:
            log.error(f"Fetch all failed: {e}")
            return []

    def update_one(
        self, collection, filter_query: dict, update_data: dict, upsert: bool = True
    ) -> bool:
        try:
            result = collection.update_one(
                filter_query, {"$set": update_data}, upsert=upsert
            )
            return result.acknowledged and result.modified_count > 0
        except PyMongoError as e:
            log.error(f"Update one failed: {e}")
            return False

    def update_many(
        self, collection, filter_query: dict, update_data: dict, upsert: bool = True
    ) -> bool:
        try:
            result = collection.update_many(
                filter_query, {"$set": update_data}, upsert=upsert
            )
            log.debug(f"Total updated: {result.modified_count}")
            return result.acknowledged and result.modified_count > 0
        except PyMongoError as e:
            log.error(f"Update many failed: {e}")
            return False

    def delete_one(self, filter_query: dict, collection) -> bool:
        try:
            result = collection.delete_one(filter_query)
            log.info(f"Deleted document: {result.deleted_count}")
            return result.acknowledged and result.deleted_count > 0
        except PyMongoError as e:
            log.error(f"Delete one failed: {e}")
            return False

    def delete_many(self, collection, filter_query: dict = {}) -> bool:
        """On defualt arg, it will delete all argument"""
        try:
            result = collection.delete_many(filter_query)
            log.info(f"Deleted all documents: {result.deleted_count}")
            return result.acknowledged and result.deleted_count > 0
        except PyMongoError as e:
            log.error(f"Delete many failed: {e}")
            return False

    def close_connection(self):
        self._client.close()


class ChatDb(MongoDb):
    _collection = None
    _chat_instance = None

    def __new__(cls, collection_name):
        if cls._chat_instance is None:
            cls._chat_instance = super().__new__(cls)
            try:
                cls._collection = cls._db[collection_name]
                log.info("MongoDB collection created successfully.")
            except PyMongoError as e:
                log.error(f"Failed to created MongoDB Collection: {e}")
                raise
        else:
            log.info("Collection is already created...")
        return cls._chat_instance

    def fetch_conversation_history(self, user_id, conversation_id):
        history = []
        for doc in self._collection.find():
            if (
                doc.get("user_id") == user_id
                and doc.get("conversation_id") == conversation_id
            ):
                history.append(doc)
        return history

    def save_chat_history(self, chat_history: dict):
        user_id = self.insert_one(chat_history, self._collection)
        log.info(f"chat history saved for user id: {user_id}")

    def __repr__(self):
        return "MongoDB"


class AuthenticatorDb(MongoDb):

    _collection = None
    _auth_instance = None
    _collection_name = None

    def __new__(cls, collection_name):
        if cls._auth_instance is None:
            cls._auth_instance = super().__new__(cls)
            cls._collection_name = collection_name
            try:
                cls._collection = cls._db[collection_name]
                log.info("MongoDB collection created successfully.")
            except PyMongoError as e:
                log.error(f"Failed to created MongoDB Collection: {e}")
                raise
        else:
            log.info("Collection is already created...")
        return cls._auth_instance

    def hash_password(self, password: str) -> bytes:
        password_bytes = password.encode(encoding="utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password.decode(encoding="utf-8")

    def verify_duplicate_user(self, user_name: str) -> bool:
        """
        Return True if user_name already exist in users collection else False
        """
        if not isinstance(user_name, str):
            raise ValueError("User name must be string!")

        query = {"userName": user_name}
        return True if self._collection.find_one(query) else False

    def insert_user_credentials(self, user_name, password):
        """For sign Up inserting user's credentials to DB"""
        user_creds = {
            "userName": user_name,
            "password": self.hash_password(password),
            "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        user_id = self.insert_one(user_creds, self._collection)
        return user_id

    def authenticate_user(self, user_name: str, password: str) -> Optional[str]:
        """
        Authenticates a user by checking username and password.

        Returns:
            if User info exist return matched user ID, otherwise None
        """
        matched_user = self.fetch_one(
            filter_query={"userName": user_name}, collection=self._collection
        )
        if not matched_user:
            st.error("E-mail not exist, please sign up.")
            log.error("E-mail not exist, please sign up.")
            return None

        password_hash = matched_user["password"]
        is_password_correct = bcrypt.checkpw(password.encode(), password_hash.encode())
        if not is_password_correct:
            log.error("Entered incorrect password!")
            st.error("Entered incorrect password!")
            return None

        return str(matched_user["_id"])
