from model.IcException import IcExcepcion
from service.RepositoryService import find_active_users, get_scope
from utils.Constants import ACTIVE_FIELD, NAME_FIELD, TTL_TOKEN
from service.CryptographyalgorithmService import FlowMode, decrypt_data
from service.GenerateAccessToken import generate_access_token
from service.PasswordHashService import verify_password

async def put_logon(user_id: str, password: str):
    user_id_dec = await decrypt_data(user_id, FlowMode.USR_AES_256_CBC)
    password_dec = await decrypt_data(password, FlowMode.PSWD_AES_256_CBC)
    l_users = await find_active_users(user_id_dec)
    l_scopes = await get_scope()
    valid_user = l_users.__len__() == 1 and verify_password(l_users[0]["password"], password_dec)
    if l_scopes.__len__() != 0 and valid_user:
        scope_parse = [scope[NAME_FIELD] for scope in l_scopes if scope[ACTIVE_FIELD]]
        return {
            "scope": scope_parse,
            "access_token": await generate_access_token(user_id_dec, scope_parse, False),
            "refresh_token": await generate_access_token(user_id_dec, scope_parse, True),
            "ttl": TTL_TOKEN
        }
    else:
        raise IcExcepcion(message="No Login", code=401)