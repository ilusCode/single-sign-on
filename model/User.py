from pydantic import BaseModel

class User(BaseModel):
    hashId: str
    active: bool

    def __init__(self, hashId: str, active: bool = True):
        # construct via BaseModel to keep pydantic behavior
        super().__init__(hashId=hashId, active=active)

    @property
    def get_hashId(self) -> str:
        return self.hashId

    @property
    def is_active(self) -> bool:
        return self.active

    @get_hashId.setter
    def get_hashId(self, value: str) -> None:
        object.__setattr__(self, 'hashId', value)

    @is_active.setter
    def is_active(self, value: bool) -> None:
        object.__setattr__(self, 'active', bool(value))