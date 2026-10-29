from utils.database import collectionUsrs, collectionScope

async def find_active_users(nickname_id: str) -> list:
    return await collectionUsrs.find({"nickname": nickname_id, "active": True}).to_list()

async def get_scope():
    return await collectionScope.find({"active": True}).to_list()
    
