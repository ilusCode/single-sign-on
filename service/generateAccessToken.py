import os
from datetime import datetime, timedelta
import jwt
from model.FlowMode import FlowMode
from service.decryptAlgorithmService import encrypt_data
from utils.Constants import ALGORITHM, TTL_TOKEN


async def generate_access_token(user_id_dec: str, scopes: list) -> str:
    now = datetime.now()
    payload = {
        "sub": await encrypt_data(user_id_dec, FlowMode.USR_AES_256_CBC),
        "scopes": await encrypt_data("|".join(scopes), FlowMode.GNL_AES_256_CBC),
        "iat": now,
        "exp": now + timedelta(seconds=TTL_TOKEN),
    }
    SECRET_KEY = os.getenv("jwt_secret_key")

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return token