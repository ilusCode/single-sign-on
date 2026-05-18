from Constants import ACTIVE_FIELD, NAME_FIELD
from service.decryptAlgorithmService import FlowMode, decrypt_data, encrypt_data
from service.getScope import get_scope

async def post_single_sign_on_info(user_id: str, password: str):
    userId = decrypt_data(user_id, FlowMode.USR_AES_256_CBC)
    password = decrypt_data(password, FlowMode.PSWD_AES_256_CBC)
    scopes = await get_scope()
    scopes = [scope[NAME_FIELD] for scope in scopes if scope[ACTIVE_FIELD]]
    return {
        "user_id": userId,
        "password": password,
        "scope": scopes,
        "token":{
            "access_token": "",
            "refresh_token": "",
            "ttl": 3600       
        }
    }
    