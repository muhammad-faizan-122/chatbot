from pymongo import MongoClient
from .utils import config
from pymongo.errors import PyMongoError
from src.common.logger import log


def get_mongo_client() -> MongoClient:
    if not hasattr(get_mongo_client, "_client"):
        try:
            get_mongo_client._client = MongoClient(host=config.host, port=config.port)
        except PyMongoError as e:
            log.error(f"Failed to Connect to MongoDB due to: {e}")
            raise
    return get_mongo_client._client


def get_database():
    client = get_mongo_client()
    return client[config.db_name]
