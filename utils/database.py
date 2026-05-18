from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "iluscodeDB"
COLLECTION_NAME = "scope_system"

client = AsyncIOMotorClient(MONGO_URI)
database = client.get_database(DATABASE_NAME)
coleccion = database.get_collection(COLLECTION_NAME)
