from pydantic import BaseModel
from typing_extensions import Annotated


class Scope(BaseModel):
    name: str
    active: bool