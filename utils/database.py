import os

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = f"mongodb://{os.getenv('mongo.username')}:{os.getenv('mongo.password')}@{os.getenv('mongo.host')}:{os.getenv('mongo.port')}"
DATABASE_NAME = DATABASE_NAME = os.getenv("mongo.db")
COLLECTION_NAME = os.getenv("mongo.collections.scope_system")
CLTN_USR_NAME = os.getenv("mongo.collections.users_hash")

client = AsyncIOMotorClient(MONGO_URI)
database = client.get_database(DATABASE_NAME)
collectionScope = database.get_collection(COLLECTION_NAME)
collectionUsrs = database.get_collection(CLTN_USR_NAME)
