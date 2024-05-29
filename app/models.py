from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, Session
from app.base import Base


follows = Table(
    'follows', Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.id')),
    Column('followed_id', Integer, ForeignKey('users.id'))
)


class User(Base):
    """Модель пользователя"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    api_key = Column(String, unique=True, index=True)
    tweets = relationship('Tweet', back_populates='owner')
    followers = relationship(
        'User', secondary=follows,
        primaryjoin=id == follows.c.follower_id,
        secondaryjoin=id == follows.c.followed_id,
        back_populates='following'
    )
    following = relationship(
        'User', secondary=follows,
        primaryjoin=id == follows.c.followed_id,
        secondaryjoin=id == follows.c.follower_id,
        back_populates='followers'
    )


class Tweet(Base):
    """Модель твита"""
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', back_populates='tweets')
    likes = relationship('Like', back_populates='tweet')
    media = relationship('Media', back_populates='tweet', cascade='all, delete-orphan')


class Like(Base):
    """Модель лайка"""
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    tweet_id = Column(Integer, ForeignKey('tweets.id'))
    tweet = relationship('Tweet', back_populates='likes')
    user = relationship('User')


class Media(Base):
    """Модель медиа"""
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    tweet_id = Column(Integer, ForeignKey('tweets.id'))
    tweet = relationship('Tweet', back_populates='media')



