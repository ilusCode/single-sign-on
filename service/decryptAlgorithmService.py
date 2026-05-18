import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from model.FlowMode import FlowMode

KEYUser = "example_key"
KEYPassword = "example_password"

def _derive_key(passphrase: str) -> bytes:
    return hashlib.sha256(passphrase.encode()).digest()

def encrypt_data(data: str, flow: FlowMode) -> str:
    """Encrypt `data` using AES-256-CBC. Returns base64(iv + ciphertext)."""
    if flow == FlowMode.USR_AES_256_CBC:
        key = _derive_key(KEYUser)
    elif flow == FlowMode.PSWD_AES_256_CBC:
        key = _derive_key(KEYPassword)
    else:
        raise ValueError("Unsupported flow mode")
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(data.encode(), AES.block_size))
    return base64.b64encode(iv + ciphertext).decode()

def decrypt_data(encrypted_data: str, flow: FlowMode) -> str:
    """Decrypt base64(iv + ciphertext) encrypted with AES-256-CBC."""
    if flow == FlowMode.USR_AES_256_CBC:
        key = _derive_key(KEYUser)
    elif flow == FlowMode.PSWD_AES_256_CBC:
        key = _derive_key(KEYPassword)
    else:
        raise ValueError("Unsupported flow mode")
    raw = base64.b64decode(encrypted_data)
    iv = raw[:16]
    ciphertext = raw[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted.decode()
