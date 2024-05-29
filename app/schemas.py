from typing import List, Optional, Dict, Union
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    api_key: str

    class Config:
        orm_mode = True


class Follower(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Following(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserProfile(BaseModel):
    id: int
    name: str
    followers: List[Follower] = []
    following: List[Following] = []

    class Config:
        orm_mode = True


class UserProfileResponse(BaseModel):
    result: bool
    user: UserProfile


class TweetCreate(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[List[int]] = None


class TweetResponse(BaseModel):
    result: bool
    tweet_id: int


class MediaUploadResponse(BaseModel):
    result: bool
    media_id: int


class TweetAuthor(BaseModel):
    id: int
    name: str


class TweetLike(BaseModel):
    user_id: int
    name: str


class Tweet(BaseModel):
    id: int
    content: str
    attachments: Optional[List[str]]
    author: TweetAuthor
    likes: Optional[List[TweetLike]]


class TweetListResponse(BaseModel):
    result: bool
    tweets: List[Tweet]


class StatusResponse(BaseModel):
    result: bool
