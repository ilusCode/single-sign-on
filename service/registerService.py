from utils.database import collectionUsrs
from model.IcException import IcExcepcion
from model.CreateUserRequest import CreateUserRequest
import json

async def put_create_account(requestBody: CreateUserRequest):
    validFindUser = await collectionUsrs.find_one({"email": (requestBody.email)})

    if validFindUser is not None:
        raise IcExcepcion(message="User already exists", code=401)
    await collectionUsrs.insert_one(vars(requestBody))
    return {"message": "Account created successfully"}