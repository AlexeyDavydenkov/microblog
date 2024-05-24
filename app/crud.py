from typing import Optional, List

from sqlalchemy.orm import Session
from app import models, schemas


def get_user_by_api_key(db: Session, api_key: str):
    return db.query(models.User).filter(models.User.api_key == api_key).first()


def create_tweet(db: Session, tweet: str, user_id: int, media_ids: Optional[List[int]] = None):
    db_tweet = models.Tweet(content=tweet, owner_id=user_id)
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet


def upload_media(file):
    # Логика загрузки файла и сохранения его в базу данных
    # Возвращает ID загруженного файла
    return 1  # пример, верните реальный ID


def delete_tweet(db: Session, tweet_id: int, user_id: int):
    tweet = db.query(models.Tweet).filter(models.Tweet.id == tweet_id, models.Tweet.owner_id == user_id).first()
    if tweet:
        db.delete(tweet)
        db.commit()
        return True
    return False


def like_tweet(db: Session, user_id: int, tweet_id: int):
    db_like = models.Like(user_id=user_id, tweet_id=tweet_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


def unlike_tweet(db: Session, user_id: int, tweet_id: int):
    like = db.query(models.Like).filter(models.Like.user_id == user_id, models.Like.tweet_id == tweet_id).first()
    if like:
        db.delete(like)
        db.commit()
        return True
    return False


def follow_user(db: Session, user_id: int, follow_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    follow_user = db.query(models.User).filter(models.User.id == follow_id).first()
    user.following.append(follow_user)
    db.commit()
    return follow_user


def unfollow_user(db: Session, user_id: int, follow_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    unfollow_user = db.query(models.User).filter(models.User.id == follow_id).first()
    user.following.remove(unfollow_user)
    db.commit()
    return True


def get_tweets_for_user(db: Session, user_id: int):
    return db.query(models.Tweet).filter(models.Tweet.owner_id == user_id).all()


def get_user_profile(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()
