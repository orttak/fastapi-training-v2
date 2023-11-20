from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id:int
    email: EmailStr
    create_at:datetime

    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # owner kismini UserOut classindan aliyoruz cunku Post un donusune User bilgisini de ekledik.
    #fastapi veriyi donerken PostBase gore donuyor. o yuzden owner olarak koyduk
    
    
class CreatePost(PostBase):
    pass

class UpdatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    #rating: Optional[int] = None

    def model_dump(self):
        return {k: v for k, v in self.model_dump().items() if v is not None}
    
class ResponsePost(PostBase):
    #inheretiance from PostBase
    id:int
    create_at:datetime
    owner_id:int
    
    class Config:
        from_attributes = True

    owner : UserOut

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

from pydantic.types import conint

class Vote(BaseModel):
    post_id:int
    dir : int
