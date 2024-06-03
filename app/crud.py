import os
from typing import List, Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app import models
from app.models import Media

UPLOAD_DIRECTORY = "./static/images"


def get_user_by_api_key(db: Session, api_key: str):
    """Возвращает пользователя по api_key"""
    return db.query(models.User).filter(models.User.api_key == api_key).first()


def create_tweet(
    db: Session, tweet: str, user_id: int, media_ids: Optional[List[int]] = None
):
    """Вносит новый твит"""
    db_tweet = models.Tweet(content=tweet, owner_id=user_id)
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)

    if media_ids:
        db.query(models.Media).filter(models.Media.id.in_(media_ids)).update(
            {models.Media.tweet_id: db_tweet.id}, synchronize_session=False
        )
        db.commit()
    return db_tweet


def upload_media(db: Session, file: UploadFile):
    """Загружает медиа, возвращает media.id"""
    if file.filename is None:
        raise ValueError("Filename cannot be None")

    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    file_url = f"/static/images/{file.filename}"

    new_media = Media(url=file_url, tweet_id=None)
    db.add(new_media)
    db.commit()
    db.refresh(new_media)

    return new_media.id


def delete_tweet(db: Session, tweet_id: int, user_id: int):
    """Удаляет твит"""
    tweet = (
        db.query(models.Tweet)
        .filter(models.Tweet.id == tweet_id, models.Tweet.owner_id == user_id)
        .first()
    )
    if tweet:
        db.delete(tweet)
        db.commit()
        return True
    return False


def like_tweet(db: Session, user_id: int, tweet_id: int):
    """ "Ставит отметку о лайке в базе"""
    db_like = models.Like(user_id=user_id, tweet_id=tweet_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


def unlike_tweet(db: Session, user_id: int, tweet_id: int):
    """ "Удаляет отметку о лайке в базе"""
    like = (
        db.query(models.Like)
        .filter(models.Like.user_id == user_id, models.Like.tweet_id == tweet_id)
        .first()
    )
    if like:
        db.delete(like)
        db.commit()
        return True
    return False


def follow_user(db: Session, user_id: int, follow_id: int):
    """Ставит отметку о подписке в базе"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise ValueError(f"User with id {user_id} not found")

    follow_user = db.query(models.User).filter(models.User.id == follow_id).first()
    if follow_user is None:
        raise ValueError(f"User with id {follow_id} not found")

    user.following.append(follow_user)
    db.commit()
    return follow_user


def unfollow_user(db: Session, user_id: int, follow_id: int):
    """Удаляет отметку о подписке в базе"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise ValueError(f"User with id {user_id} not found")

    unfollow_user = db.query(models.User).filter(models.User.id == follow_id).first()
    if unfollow_user is None:
        raise ValueError(f"User with id {follow_id} not found")

    user.following.remove(unfollow_user)
    db.commit()
    return True


def get_user_profile(db: Session, user_id: int):
    """Возвращает информацию о профиле"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None
    # Собрать подписчиков и подписки
    followers = [
        {"id": follower.id, "name": follower.name} for follower in user.followers
    ]
    following = [
        {"id": following.id, "name": following.name} for following in user.following
    ]
    return {
        "id": user.id,
        "name": user.name,
        "followers": followers,
        "following": following,
    }


def get_all_tweets(db: Session):
    """Возвращает информацию о твитах"""
    return db.query(models.Tweet).all()
