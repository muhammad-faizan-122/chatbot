from typing import List, Optional
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from src.common.logger import log


class MongoRepository:
    def insert_one(self, doc: dict, collection: Collection) -> str:
        try:
            result = collection.insert_one(doc)
            return str(result.inserted_id)
        except PyMongoError as e:
            log.error(f"Insert failed: {e}")
            raise

    def insert_many(self, docs: list[dict], collection: Collection) -> bool:
        try:
            result = collection.insert_many(docs)
            return bool(result.inserted_ids)
        except PyMongoError as e:
            log.error(f"Insert many failed: {e}")
            return False

    def fetch_one(self, filter_query: dict, collection: Collection) -> Optional[dict]:
        try:
            return collection.find_one(filter_query)
        except PyMongoError as e:
            log.error(f"Fetch one failed: {e}")
            return None

    def fetch_all(self, collection: Collection) -> List[dict]:
        try:
            return list(collection.find())
        except PyMongoError as e:
            log.error(f"Fetch all failed: {e}")
            return []

    def update_one(
        self,
        collection: Collection,
        filter_query: dict,
        update_data: dict,
        upsert: bool = True,
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
        self,
        collection: Collection,
        filter_query: dict,
        update_data: dict,
        upsert: bool = True,
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

    def delete_one(self, filter_query: dict, collection: Collection) -> bool:
        try:
            result = collection.delete_one(filter_query)
            return result.acknowledged and result.deleted_count > 0
        except PyMongoError as e:
            log.error(f"Delete one failed: {e}")
            return False

    def delete_many(self, collection: Collection, filter_query: dict = {}) -> bool:
        try:
            result = collection.delete_many(filter_query)
            return result.acknowledged and result.deleted_count > 0
        except PyMongoError as e:
            log.error(f"Delete many failed: {e}")
            return False
