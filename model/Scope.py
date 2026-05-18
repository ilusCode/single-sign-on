from pydantic import AfterValidator, BaseModel
from bson import ObjectId as _ObjectId
from typing_extensions import Annotated

def check_object_id(value: str) -> str:
    if not _ObjectId.is_valid(value):
        raise ValueError('Invalid ObjectId')
    return value

class Scope(BaseModel):
    id: Annotated[str, AfterValidator(check_object_id)]
    name: str
    active: bool