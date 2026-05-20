from utils.database import collectionScope

async def get_scope():
    return await collectionScope.find({"active": True}).to_list()
    
