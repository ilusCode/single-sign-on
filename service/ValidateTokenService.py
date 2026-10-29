import jwt
import os

from utils.Constants import ALGORITHM
from dotenv import load_dotenv
from service.CryptographyalgorithmService import FlowMode, decrypt_data

load_dotenv()

async def validate_token(token: str):
    token = token.replace("Bearer ", "")
    SECRET_KEY = os.getenv("jwt_secret_key")
    try:
        jwtDec = jwt.decode(token, algorithms=[ALGORITHM], key=SECRET_KEY)
        # Decrypting the claims checks they were encrypted with our keys (raises IcExcepcion 400 otherwise)
        await decrypt_data(jwtDec["sub"], FlowMode.USR_AES_256_CBC)
        await decrypt_data(jwtDec["scopes"], FlowMode.GNL_AES_256_CBC)
    except jwt.ExpiredSignatureError as e:
        print(f"Token has expired: {e}")
        return {"is_valid": False, "message": "Token has expired"}
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
        return {"is_valid": False, "message": "Invalid token"}
    return {"is_valid": True, "payload": jwtDec}