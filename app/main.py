from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from typing import List, Optional
from sqlalchemy.orm import Session
from app import models, schemas, crud, db

app = FastAPI()


# Зависимости для получения сессии базы данных
# def get_db():
#     db = db.SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# Примеры эндпоинтов
# @app.post("/api/tweets")
# async def create_tweet(api_key: str, tweet_data: str, tweet_media_ids: Optional[List[int]] = None,
#                        db: Session = Depends(get_db)):
#     user = crud.get_user_by_api_key(db, api_key=api_key)
#     if not user:
#         raise HTTPException(status_code=400, detail="Invalid API Key")
#     tweet = crud.create_tweet(db=db, tweet=tweet_data, user_id=user.id, media_ids=tweet_media_ids)
#     return {"result": True, "tweet_id": tweet.id}
#
#
# @app.post("/api/medias")
# async def upload_media(api_key: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
#     user = crud.get_user_by_api_key(db, api_key=api_key)
#     if not user:
#         raise HTTPException(status_code=400, detail="Invalid API Key")
#     media_id = crud.upload_media(file=file)
#     return {"result": True, "media_id": media_id}
#
#
# @app.delete("/api/tweets/{id}")
# async def delete_tweet(id: int, api_key: str, db: Session = Depends(get_db)):
#     user = crud.get_user_by_api_key(db, api_key=api_key)
#     if not user:
#         raise HTTPException(status_code=400, detail="Invalid API Key")
#     success = crud.delete_tweet(db=db, tweet_id=id, user_id=user.id)
#     if not success:
#         raise HTTPException(status_code=400, detail="Tweet not found or unauthorized")
#     return {"result": True}
#
#
# @app.post("/api/tweets/{id}/likes")
# async def like_tweet(id: int, api_key: str, db: Session = Depends(get_db)):
#     user = crud.get_user_by_api_key(db, api_key=api_key)
#     if not user:
#         raise HTTPException(status_code=400, detail="Invalid API Key")
#     like = crud.like_tweet(db=db, user_id=user.id, tweet_id=id)
#     return {"result": True}
#
#
# @app.delete("/api/tweets/{id}/likes")
# async def unlike_tweet(id: int, api_key: str, db: Session = Depends(get_db)):
#     user = crud.get_user_by_api_key(db, api_key=api_key)
#     if not user:
#         raise HTTPException(status_code=400, detail="Invalid API Key")
#     success = crud.unlike_tweet(db=db, user_id=user.id, tweet_id=id)
#     if not success:
#         raise HTTPException(status_code=400, detail="Like not found or unauthorized")
#     return {"result": True}
#
#
# @app.post("/api/users/{id}/follow")
# async def follow_user(id: int, api_key: str, db: Session = Depends(get_db)):
#     user = crud.get_user_by_api_key(db, api_key=api_key)
#     if not user:
#         raise HTTPException(status_code=400, detail="Invalid API Key")
#     follow = crud.follow_user(db=db, user_id=user.id, follow_id=id)
#     return {"result": True}
#
#
# @app.delete("/api/users/{id}/follow")
# async def unfollow_user(id: int, api_key: str, db: Session = Depends(get_db)):
#     user = crud.get_user_by_api_key(db, api_key=api_key)
#     if not user:
#         raise HTTPException(status_code=400, detail="Invalid API Key")
#     success = crud.unfollow_user(db=db, user_id=user.id, follow_id=id)
#     if not success:
#         raise HTTPException(status_code=400, detail="Unfollow failed or unauthorized")
#     return {"result": True}
#
#
# @app.get("/api/tweets")
# async def get_tweets(api_key: str, db: Session = Depends(get_db)):
#     user = crud.get_user_by_api_key(db, api_key=api_key)
#     if not user:
#         raise HTTPException(status_code=400, detail="Invalid API Key")
#     tweets = crud.get_tweets_for_user(db=db, user_id=user.id)
#     return {"result": True, "tweets": tweets}


@app.get("/api/users/me", response_model=schemas.ResponseModel)
async def get_my_profile(db: Session = Depends(db.get_db)):
    # user = crud.get_user_by_api_key(db, api_key=api_key)
    # print(user)
    # if not user:
    #     return ({'result': False, 'error_type': 'InvalidAPIKey', 'error_message': 'Invalid API key.'}), 403

    user = {
        "id": 3,
        "name": "str",
        "followers": [{"id": 3, "name": "str"}],
        "following": [{"id": 3, "name": "str"}]
    }

    return {"result": "true", "user": user}


    # if not user:
    #     raise HTTPException(status_code=400, detail="Invalid API Key")
    # profile = crud.get_user_profile(db=db, user_id=user.id)
    # return {"result": True, "user": profile}


# @app.get("/api/users/{id}")
# async def get_user_profile(id: int, db: Session = Depends(get_db)):
#     profile = crud.get_user_profile(db=db, user_id=id)
#     return {"result": True, "user": profile}
