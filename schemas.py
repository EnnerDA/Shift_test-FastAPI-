from pydantic import BaseModel
from datetime import date


class User(BaseModel):
    username: str
    password: str

class UserInfo(User):
    salary: float
    salary_increase_date: date|None = None