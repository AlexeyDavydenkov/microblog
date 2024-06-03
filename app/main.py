from typing import Optional

from fastapi import Depends, FastAPI, File, Header, HTTPException, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.db import engine, get_db, init_db
from app.schemas import MediaUploadResponse, StatusResponse, TweetCreate, TweetResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

init_db()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Обработчик для HTTPException"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "result": False,
            "error_type": "HTTPException",
            "error_message": exc.detail,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Обработчик для ValidationError"""
    return JSONResponse(
        status_code=422,
        content={
            "result": False,
            "error_type": "ValidationError",
            "error_message": exc.errors(),
        },
    )


@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    """Обработчик возможных исключений"""
    return JSONResponse(
        status_code=500,
        content={
            "result": False,
            "error_type": type(exc).__name__,
            "error_message": str(exc),
        },
    )


@app.post("/api/tweets", response_model=TweetResponse)
async def create_tweet(
    tweet: TweetCreate,
    api_key: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """
    Создает новый твит
    :param:
        api-key: str
        tweet_data: str
        tweet_media_ids: []
    :return:
        json: id созданного твита
    """
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key is required")
    user = crud.get_user_by_api_key(db, api_key=api_key)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid API Key")
    tweet_db = crud.create_tweet(
        db=db, tweet=tweet.tweet_data, user_id=user.id, media_ids=tweet.tweet_media_ids
    )
    return {"result": True, "tweet_id": tweet_db.id}


@app.post("/api/medias", response_model=MediaUploadResponse)
async def upload_media(
    api_key: Optional[str] = Header(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Загружает файл
    :param:
        api-key: str
        form: file=”image.jpg”
    :return:
        json: id id загруженного файла
    """
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key is required")
    user = crud.get_user_by_api_key(db, api_key=api_key)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid API Key")
    media_id = crud.upload_media(file=file, db=db)
    return {"result": True, "media_id": media_id}


@app.delete("/api/tweets/{id}", response_model=StatusResponse)
async def delete_tweet(
    id: int, api_key: Optional[str] = Header(None), db: Session = Depends(get_db)
):
    """
    Удаляет твит
    :param:
        api-key: str
    :return:
        json: сообщение о статусе операции
    """
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key is required")
    user = crud.get_user_by_api_key(db, api_key=api_key)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid API Key")
    success = crud.delete_tweet(db=db, tweet_id=id, user_id=user.id)
    if not success:
        raise HTTPException(status_code=400, detail="Tweet not found or unauthorized")
    return {"result": True}


@app.post("/api/tweets/{id}/likes", response_model=StatusResponse)
async def like_tweet(
    id: int, api_key: Optional[str] = Header(None), db: Session = Depends(get_db)
):
    """
    Ставит отметку «Нравится» на твит
    :param:
        api-key: str
    :return:
        json: сообщение о статусе операции
    """
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key is required")
    user = crud.get_user_by_api_key(db, api_key=api_key)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid API Key")
    crud.like_tweet(db=db, user_id=user.id, tweet_id=id)
    return {"result": True}


@app.delete("/api/tweets/{id}/likes", response_model=StatusResponse)
async def unlike_tweet(
    id: int, api_key: Optional[str] = Header(None), db: Session = Depends(get_db)
):
    """
    Убирает отметку «Нравится» на твит
    :param:
        api-key: str
    :return:
        json: сообщение о статусе операции
    """
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key is required")
    user = crud.get_user_by_api_key(db, api_key=api_key)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid API Key")
    success = crud.unlike_tweet(db=db, user_id=user.id, tweet_id=id)
    if not success:
        raise HTTPException(status_code=400, detail="Like not found or unauthorized")
    return {"result": True}


@app.post("/api/users/{id}/follow", response_model=StatusResponse)
async def follow_user(
    id: int, api_key: Optional[str] = Header(None), db: Session = Depends(get_db)
):
    """
    Подписка на другого пользователя
    :param:
        api-key: str
    :return:
        json: сообщение о статусе операции
    """
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key is required")
    user = crud.get_user_by_api_key(db, api_key=api_key)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid API Key")
    crud.follow_user(db=db, user_id=user.id, follow_id=id)
    return {"result": True}


@app.delete("/api/users/{id}/follow", response_model=StatusResponse)
async def unfollow_user(
    id: int, api_key: Optional[str] = Header(None), db: Session = Depends(get_db)
):
    """
    Отписка от другого пользователя
    :param:
        api-key: str
    :return:
        json: сообщение о статусе операции
    """
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key is required")
    user = crud.get_user_by_api_key(db, api_key=api_key)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid API Key")
    success = crud.unfollow_user(db=db, user_id=user.id, follow_id=id)
    if not success:
        raise HTTPException(status_code=400, detail="Unfollow failed or unauthorized")
    return {"result": True}


@app.get("/api/tweets", response_model=schemas.TweetListResponse)
async def get_tweets(
    api_key: Optional[str] = Header(None), db: Session = Depends(get_db)
):
    """
    Получает ленту с твитами
    :param:
        api-key: str
    :return:
        json: список твитов для ленты этого пользователя
    """
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key is required")
    user = crud.get_user_by_api_key(db, api_key=api_key)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid API Key")

    tweets = crud.get_all_tweets(db=db)
    formatted_tweets = []
    for tweet in tweets:
        formatted_tweet = {
            "id": tweet.id,
            "content": tweet.content,
            "attachments": [media.url for media in tweet.media],
            "author": {
                "id": tweet.owner.id,
                "name": tweet.owner.name,
            },
            "likes": [
                {"user_id": like.user_id, "name": like.user.name}
                for like in tweet.likes
            ],
        }
        formatted_tweets.append(formatted_tweet)
    return {"result": True, "tweets": formatted_tweets}


@app.get("/api/users/me", response_model=schemas.UserProfileResponse)
async def get_my_profile(
    api_key: Optional[str] = Header(None), db: Session = Depends(get_db)
):
    """
    Получает информацию о своём профиле
    :param:
        api-key: str
    :return:
        json: информация о профиле
    """
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key is required")

    user = crud.get_user_by_api_key(db, api_key=api_key)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid API Key")

    profile = crud.get_user_profile(db=db, user_id=user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    return {"result": True, "user": profile}


@app.get("/api/users/{id}", response_model=schemas.UserProfileResponse)
async def get_user_profile(id: int, db: Session = Depends(get_db)):
    """
    Получает информацию о профиле по id
    :param:
        id: int
    :return:
        json: информация о профиле
    """
    profile = crud.get_user_profile(db=db, user_id=id)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    return {"result": True, "user": profile}
