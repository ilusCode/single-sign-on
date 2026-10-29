# 🔐 Single Sign-On

Servicio de autenticación (**Single Sign-On**) construido con **FastAPI** y **MongoDB**. Permite
registrar usuarios, iniciar sesión con credenciales cifradas con **AES-256-CBC** y emitir y validar
tokens **JWT** que incluyen los *scopes* activos del sistema.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?logo=jsonwebtokens&logoColor=white)

> 🚧 **Proyecto en desarrollo.** Revisa [Estado y pendientes](#-estado-y-pendientes) antes de usarlo en producción.

---

## 🏗️ Cómo funciona

```
Cliente                                   SSO (FastAPI)                         MongoDB
  │ PUT /api/logon                          │                                     │
  │ x-user-iluscode: AES(usuario)  ───────▶ │ descifra usuario y contraseña       │
  │ x-pw-iluscode:   AES(contraseña)        │ ───── busca usuario activo ───────▶ │ users_hash
  │                                         │ ───── lee scopes activos ─────────▶ │ scope_system
  │ ◀──── access_token + refresh_token ──── │ firma JWT (HS256)                   │
  │                                         │                                     │
  │ GET /api/validate                       │                                     │
  │ Authorization: Bearer <token>  ───────▶ │ verifica firma y expiración         │
  │ ◀──── { is_valid, payload } ─────────── │                                     │
```

### Cifrado

Las credenciales viajan cifradas con **AES-256-CBC**, en formato `base64(iv + ciphertext)` con un IV
aleatorio de 16 bytes. La clave AES es el `SHA-256` de una frase secreta, y cada tipo de dato usa la suya:

| Flujo (`FlowMode`) | Variable de entorno | Se usa para |
|--------------------|---------------------|-------------|
| `USR_AES_256_CBC` | `usr_secret_key` | Usuario (header `x-user-iluscode` y claim `sub`) |
| `PSWD_AES_256_CBC` | `psw_secret_key` | Contraseña (header `x-pw-iluscode`) |
| `GNL_AES_256_CBC` | `gnr_secret_key` | Claims `scopes` y `ref` del token |

### Token JWT

Firmado con **HS256** (`jwt_secret_key`). El payload contiene:

| Claim | Contenido |
|-------|-----------|
| `sub` | Usuario, cifrado con `USR_AES_256_CBC` |
| `scopes` | Scopes activos separados por `\|`, cifrados con `GNL_AES_256_CBC` |
| `ref` | `"True"` si es *refresh token*, `"False"` si es *access token* (cifrado) |
| `iat` / `exp` | Emisión y expiración (timestamp). Vigencia: `TTL_TOKEN` = 60 000 ms (60 s) |

## 📡 API

| Método | Ruta | Descripción |
|--------|------|-------------|
| `PUT` | `/api/register` | Crea una cuenta de usuario |
| `PUT` | `/api/logon` | Inicia sesión y devuelve los tokens |
| `GET` | `/api/validate` | Valida un token JWT |
| `GET` | `/default` | Comprobación de vida (`{"Hello": "World"}`) |

FastAPI genera la documentación interactiva en `/docs` (Swagger UI) y `/redoc`.

### `PUT /api/register`

```json
{
  "email": "eduardo@example.com",
  "password": "...",
  "nickname": "eduardo",
  "name": "Eduardo",
  "lastname": "Fernández",
  "country": "MX",
  "active": true
}
```

| Respuesta | Cuándo |
|-----------|--------|
| `200` `{"message": "Account created successfully"}` | Cuenta creada |
| `401` `{"message": "User already exists"}` | Ya existe un usuario con ese `email` |

### `PUT /api/logon`

| Header | Valor |
|--------|-------|
| `x-user-iluscode` | `nickname` cifrado con `USR_AES_256_CBC` |
| `x-pw-iluscode` | Contraseña cifrada con `PSWD_AES_256_CBC` |

**`200 OK`**

```json
{
  "scope": ["read", "write"],
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "ttl": 60000
}
```

| Error | Cuándo |
|-------|--------|
| `400` | Un header no se puede descifrar |
| `401` `{"message": "No Login"}` | Credenciales incorrectas, usuario inactivo o sin scopes activos |

### `GET /api/validate`

| Header | Valor |
|--------|-------|
| `Authorization` | `Bearer <token>` |

```json
{ "is_valid": true, "payload": { "sub": "...", "scopes": "...", "iat": 1780000000.0, "exp": 1780000060.0, "ref": "..." } }
```

```json
{ "is_valid": false, "message": "Token has expired" }
```

### Cifrar credenciales para probar

```python
import base64, hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

def encrypt(data: str, passphrase: str) -> str:
    key = hashlib.sha256(passphrase.encode()).digest()
    iv = get_random_bytes(16)
    ct = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(data.encode(), AES.block_size))
    return base64.b64encode(iv + ct).decode()

print(encrypt("eduardo", "<usr_secret_key>"))   # -> x-user-iluscode
print(encrypt("mi-pass", "<psw_secret_key>"))   # -> x-pw-iluscode
```

## ⚙️ Configuración

El servicio lee la configuración de variables de entorno o de un archivo `.env` (ignorado por git):

```dotenv
# MongoDB
mongo.username=
mongo.password=
mongo.host=localhost
mongo.port=27017
mongo.db=iluscodeDB
mongo.collections.scope_system=scope_system
mongo.collections.users_hash=users_hash

# Claves (usa valores largos y aleatorios)
usr_secret_key=
psw_secret_key=
gnr_secret_key=
jwt_secret_key=
```

### Colecciones de MongoDB

| Colección | Documento |
|-----------|-----------|
| `users_hash` | `{ email, password, nickname, name, lastname, country, active }` |
| `scope_system` | `{ name, active }` (se incluyen en el token todos los scopes con `active: true`) |

## 🚀 Ejecución local

```bash
python -m venv .venv
source .venv/bin/activate
pip install "fastapi[standard]" motor pycryptodome PyJWT python-dotenv
fastapi dev main.py
```

La API queda en `http://127.0.0.1:8000` y su documentación en `http://127.0.0.1:8000/docs`.

## 📁 Estructura

```
├── main.py                              # Rutas FastAPI y manejador de IcExcepcion
├── model/                               # CreateUserRequest, FlowMode, IcException, Scope, User
├── service/
│   ├── CryptographyalgorithmService.py  # Cifrado/descifrado AES-256-CBC
│   ├── GenerateAccessToken.py           # Emisión de JWT
│   ├── LogonService.py                  # Flujo de login
│   ├── RegisterService.py               # Alta de usuarios
│   ├── RepositoryService.py             # Consultas a MongoDB
│   └── ValidateTokenService.py          # Validación de JWT
└── utils/
    ├── Constants.py                     # TTL_TOKEN, ALGORITHM, nombres de campos
    └── database.py                      # Cliente Motor (MongoDB asíncrono)
```

## 🚧 Estado y pendientes

- [ ] **Contraseñas sin hash:** `/api/register` guarda la contraseña tal cual, y el login la compara en texto plano. Conviene guardarla con `bcrypt` o `argon2`.
- [ ] **Datos sensibles en los logs:** varios `print` muestran el token completo, el texto antes de cifrarlo (incluida la contraseña) y los datos descifrados.
- [ ] **Sin `requirements.txt`** ni pruebas automatizadas.
- [ ] **Refresh token:** se emite, pero todavía no hay endpoint para renovar el access token, y los dos tienen la misma vigencia.
- [ ] `.gitlab-ci.yml` viene de GitLab y no se ejecuta en GitHub. Hay que migrarlo a GitHub Actions o eliminarlo.

## 👤 Autor

**Eduardo Fernández Morales** — [@ilusCode](https://github.com/ilusCode) · [LinkedIn](https://www.linkedin.com/in/eduardo-fernandez-morales/)
