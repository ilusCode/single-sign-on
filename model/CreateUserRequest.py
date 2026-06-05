from dataclasses import dataclass

@dataclass
class CreateUserRequest:
    email: str = ""
    password: str = ""
    nickname: str = ""
    name: str = ""
    lastname: str = ""
    country: str = ""
    active: bool = True
