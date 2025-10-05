import os
import sys

sys.path.append(os.getcwd())
from src.db.mongodb import Authenticator
from datetime import datetime


db = Authenticator(db_name="bot", collection_name="users")


doc = {
    "userName": "muhfaizan2k23",
    "password": db.hash_password("Hi"),
    "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}

doc["lastLogin"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# id = db.insert_one(doc)
# print(id)

doc = {
    "userName": "muhfaizan",
    "password": db.hash_password("Hi"),
    "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}


doc = {
    "userName": "muhfaizan",
    "password": "Hi",
    "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}

user_name = doc["userName"]
password = doc["password"]

#
# if db.is_username_already_exist(doc["userName"]):

#     query = {"userName": user_name, "password": password}
#     # password = pass
#     user_info = db.fetch_one(query)
#     user_id = user_info.get("_id", "") if user_info else ""

#     if not user_id:
#         raise

#     print("user id: ", user_id, type(user_id))


# else:

#     user_id = db.insert_one(doc)
#     print(user_id)
#     if not user_id:
#         raise "Failed to add user in users Collection"
#     print("added user")


# testing authenticate user function

# user_name = input("Enter user name: ")
# password = input("Enter password: ")


# user_id = db.authenticate_user(user_name, password)

# print(user_id)
