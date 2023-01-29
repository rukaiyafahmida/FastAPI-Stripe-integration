from pydantic import BaseModel


class User(BaseModel):
    first_name: str
    last_name: str
    user_email: str
