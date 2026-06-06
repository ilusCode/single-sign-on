from utils.database import collectionUsrs, collectionScope

async def valid_hash_id(nickname_id: str, pass_id: str) -> list:
    return await collectionUsrs.find({"nickname": nickname_id, "password": pass_id, "active": True}).to_list()

async def get_scope():
    return await collectionScope.find({"active": True}).to_list()
    
