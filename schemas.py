from typing import List, Optional

from pydantic import BaseModel

class JokeBase(BaseModel):
    text: Optional[str] = None

class JokeCreate(JokeBase):
    pass

class Joke(JokeBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class JokeUpdate(JokeBase):
    text: str

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    jokes: List[Joke] = [] 

    class Config:
        orm_mode = True
