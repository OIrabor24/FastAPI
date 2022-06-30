from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from App.database import Base

from pydantic.types import conint

class PostBase(BaseModel):
    title: str 
    content: str 
    published: bool = True # if the user doesnt provide published, then it defaults to true
    # rating: Optional[int] = None # fully optional field, defaults to none if not provided

class PostCreate(PostBase): #Inheritance
    pass 


class UserCreate(BaseModel):
    email: EmailStr
    password: str 

class UserOut(BaseModel):
    id: int 
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True 

class UserLogin(BaseModel):
    email: EmailStr
    password: str 
 
class Post(PostBase): #this is our JSON Response class!
    id: int
    created_at: datetime
    owner_id: int 
    owner: UserOut 

    class Config: #Pydantic's orm_mode will tell the model to read the data even if it;s not a dict
        orm_mode = True 

class PostOut(BaseModel):
    Post: Post #inheritance from Post class above
    votes: int 

class Token(BaseModel):
    access_token: str 
    token_type: str 

class TokenData(BaseModel):
    id: Optional[str] = None 
    

class Vote(BaseModel):
    post_id: int 
    dir: conint(le=1) #course names this dir