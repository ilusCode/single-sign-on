from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = ""
DATABASE_NAME = ""
COLLECTION_NAME = ""

client = AsyncIOMotorClient(MONGO_URI)
database = client.get_database(DATABASE_NAME)
coleccion = database.get_collection(COLLECTION_NAME)
