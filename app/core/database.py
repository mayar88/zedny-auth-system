import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

class Database:
    def __init__(self):
        self.MONGO_URI = os.getenv("MONGO_URI")
        self.DB_NAME = os.getenv("DB_NAME")
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

        self.client = MongoClient(self.MONGO_URI)
        self.db = self.client[self.DB_NAME]

        self.users = self.db["users"]
        self.instructors = self.db["instructors"]
        self.sessions = self.db["sessions"]
