from pymongo import MongoClient
from .utils import config


def get_mongo_client() -> MongoClient:
    if not hasattr(get_mongo_client, "_client"):
        get_mongo_client._client = MongoClient(host=config.host, port=config.port)
    return get_mongo_client._client


def get_database():
    client = get_mongo_client()
    return client[config.db_name]
