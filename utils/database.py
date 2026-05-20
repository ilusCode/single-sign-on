from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "iluscodeDB"
COLLECTION_NAME = "scope_system"
CLTN_USR_NAME = "users_hash"

client = AsyncIOMotorClient(MONGO_URI)
database = client.get_database(DATABASE_NAME)
collectionScope = database.get_collection(COLLECTION_NAME)
collectionUsrs = database.get_collection(CLTN_USR_NAME)
