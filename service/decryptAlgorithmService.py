import base64
import hashlib
import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from model.FlowMode import FlowMode
from model.IcException import IcExcepcion
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY_USER : str = os.getenv("usr_secret_key", None)
SECRET_KEY_PSW : str = os.getenv("psw_secret_key", None)
SECRET_KEY_GNR : str = os.getenv("gnr_secret_key", None)

def _derive_key(passphrase: str) -> bytes:
    return hashlib.sha256(passphrase.encode()).digest()

async def encrypt_data(data: str, flow: FlowMode) -> str:
    print(f"Encrypt `{data}` using AES-256-CBC. Returns base64(iv + ciphertext).")
    try:
        key = select_key_by_flow_mode(flow)
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(data.encode(), AES.block_size))    
        return base64.b64encode(iv + ciphertext).decode()
    except Exception as e:
        print(f"Encryption error: {e}")
        raise IcExcepcion(message=f"{e}", code=400)

def select_key_by_flow_mode(flow: FlowMode) -> bytes:
    if flow == FlowMode.USR_AES_256_CBC:
        key = _derive_key(SECRET_KEY_USER)
    elif flow == FlowMode.PSWD_AES_256_CBC:
        key = _derive_key(SECRET_KEY_PSW)
    elif flow == FlowMode.GNL_AES_256_CBC:
        key = _derive_key(SECRET_KEY_GNR)
    else:
        raise IcExcepcion("Unsupported flow mode")
    return key
    
async def decrypt_data(encrypted_data: str, flow: FlowMode) -> str:
    print(f"Decrypt base64(iv + ciphertext) encrypted with AES-256-CBC.")
    try:
        key = select_key_by_flow_mode(flow)
        raw = base64.b64decode(encrypted_data)
        iv = raw[:16]
        ciphertext = raw[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted.decode()
    except Exception as e:
        print(f"Decryption error: {e}")
        raise IcExcepcion(message=f"{e}", code=400)