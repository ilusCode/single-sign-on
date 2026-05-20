from utils.database import collectionUsrs

async def valid_hash_id(hash_id: str, pass_id: str) -> list:
    return await collectionUsrs.find({"hashId": hash_id, "passId": pass_id, "active": True}).to_list()
