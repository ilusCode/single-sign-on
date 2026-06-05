from model.IcException import IcExcepcion
from service.getUser import valid_hash_id
from utils.Constants import ACTIVE_FIELD, NAME_FIELD, TTL_TOKEN
from service.decryptAlgorithmService import FlowMode, decrypt_data, encrypt_data
from service.getScope import get_scope
from service.generateAccessToken import generate_access_token

async def put_logon(user_id: str, password: str):
    user_id_dec = await decrypt_data(user_id, FlowMode.USR_AES_256_CBC)
    password_dec = await decrypt_data(password, FlowMode.PSWD_AES_256_CBC)
    l_users = await valid_hash_id(user_id_dec, password_dec)
    l_scopes = await get_scope()
    if l_scopes.__len__() != 0 and l_users.__len__() != 0 and l_users.__len__() <= 1:
        scope_parse = [scope[NAME_FIELD] for scope in l_scopes if scope[ACTIVE_FIELD]]
        return {
            "scope": scope_parse,
            "access_token": await generate_access_token(user_id_dec, scope_parse),
            "refresh_token": "",
            "ttl": TTL_TOKEN
        }
    else:
        raise IcExcepcion(message="No Login", code=401)