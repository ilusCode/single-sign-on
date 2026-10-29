from utils.database import collectionUsrs
from model.IcException import IcExcepcion
from model.CreateUserRequest import CreateUserRequest
from service.PasswordHashService import hash_password

async def put_create_account(requestBody: CreateUserRequest):
    validFindUser = await collectionUsrs.find_one({"email": (requestBody.email)})

    if validFindUser is not None:
        raise IcExcepcion(message="User already exists", code=401)
    user = {**vars(requestBody), "password": hash_password(requestBody.password)}
    await collectionUsrs.insert_one(user)
    return {"message": "Account created successfully"}