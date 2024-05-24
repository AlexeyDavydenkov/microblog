from pydantic import BaseModel
from typing import List, Optional


class TweetBase(BaseModel):
    content: str


class TweetCreate(TweetBase):
    pass


class Tweet(TweetBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    pass


class Follower(BaseModel):
    id: int
    name: str


class User(UserBase):
    id: int
    name: str
    followers: List[Follower]
    following: List[Follower]

    class Config:
        orm_mode = True


class ResponseModel(BaseModel):
    result: str
    user: User


class LikeBase(BaseModel):
    pass


class LikeCreate(LikeBase):
    user_id: int
    tweet_id: int


class Like(LikeBase):
    id: int

    class Config:
        orm_mode = True
