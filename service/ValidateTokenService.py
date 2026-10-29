import jwt
import os

from datetime import datetime
from utils.Constants import ALGORITHM
from dotenv import load_dotenv
from service.CryptographyalgorithmService import FlowMode, decrypt_data

load_dotenv()

async def validate_token(token: str):
    print(f"Validating token `{token}`")
    token = token.replace("Bearer ", "")
    SECRET_KEY = os.getenv("jwt_secret_key")
    try:
        now = datetime.now()
        print(f"now: {now}")
        jwtDec = jwt.decode(token, algorithms=[ALGORITHM], key=SECRET_KEY)
        print(f"Decoded token: {jwtDec.keys()}")
        sub = await decrypt_data(jwtDec["sub"], FlowMode.USR_AES_256_CBC)
        scopes = await decrypt_data(jwtDec["scopes"], FlowMode.GNL_AES_256_CBC)
        exp = jwtDec["exp"]
        iat = jwtDec["iat"]
        print(f"Decoded exp: {datetime.fromtimestamp(exp)}, iat: {datetime.fromtimestamp(iat)}")
        print(f"Decrypted sub: {sub}")
        print(f"Decrypted scopes: {scopes}")
    except jwt.ExpiredSignatureError as e:
        print(f"Token has expired: {e}")
        return {"is_valid": False, "message": "Token has expired"}
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
        return {"is_valid": False, "message": "Invalid token"}
    return {"is_valid": True, "payload": jwtDec}