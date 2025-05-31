from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TokenData(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ArticleBase(BaseModel):
    title: str
    content: str

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    title: Optional[str] = None
    content: Optional[str] = None

class Article(ArticleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int

    class Config:
        from_attributes = True

class ArticleWithViews(Article):
    view_count: int

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True