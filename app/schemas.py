from datetime import datetime
from typing import Literal, Optional

from pydantic import AliasChoices, BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut


class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    post: Post = Field(validation_alias=AliasChoices("Post", "post"))
    votes: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]
