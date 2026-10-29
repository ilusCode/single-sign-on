from pydantic import BaseModel

class Scope(BaseModel):
    name: str
    active: bool