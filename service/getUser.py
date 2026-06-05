from utils.database import collectionUsrs

async def valid_hash_id(nickname_id: str, pass_id: str) -> list:
    return await collectionUsrs.find({"nickname": nickname_id, "password": pass_id, "active": True}).to_list()
