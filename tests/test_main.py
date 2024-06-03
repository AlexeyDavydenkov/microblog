from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud


def test_create_tweet(client: TestClient, db_session: Session, create_test_users):
    user1, _ = create_test_users
    response = client.post(
        "/api/tweets",
        json={"tweet_data": "This is a test tweet", "tweet_media_ids": []},
        headers={"api-key": user1.api_key},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert data["tweet_id"] == 1


def test_create_tweet_no_api_key(client: TestClient):
    response = client.post(
        "/api/tweets",
        json={"tweet_data": "This is a test tweet", "tweet_media_ids": []},
    )
    assert response.status_code == 400
    assert response.json()["error_message"] == "API Key is required"


def test_create_tweet_invalid_api_key(client: TestClient, db_session: Session):
    invalid_api_key = "invalid_key"
    response = client.post(
        "/api/tweets",
        headers={"api-key": invalid_api_key},
        json={"tweet_data": "This is a test tweet", "tweet_media_ids": []},
    )
    assert response.status_code == 400
    assert response.json()["error_message"] == "Invalid API Key"


def test_upload_media(client: TestClient, db_session: Session, create_test_users):
    user1, _ = create_test_users
    with open("tests/test_image.jpg", "rb") as img:
        response = client.post(
            "/api/medias", files={"file": img}, headers={"api-key": user1.api_key}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert "media_id" in data


def test_delete_tweet(client: TestClient, db_session: Session, create_test_users):
    user1, _ = create_test_users
    tweet = crud.create_tweet(
        db_session, tweet="Test tweet to be deleted", user_id=user1.id
    )
    response = client.delete(
        f"/api/tweets/{tweet.id}", headers={"api-key": user1.api_key}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True


def test_like_tweet(client: TestClient, db_session: Session, create_test_users):
    user1, user2 = create_test_users
    tweet = crud.create_tweet(
        db_session, tweet="Test tweet to be liked", user_id=user1.id
    )
    response = client.post(
        f"/api/tweets/{tweet.id}/likes", headers={"api-key": user2.api_key}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True


def test_unlike_tweet(client: TestClient, db_session: Session, create_test_users):
    user1, user2 = create_test_users
    tweet = crud.create_tweet(
        db_session, tweet="Test tweet to be unliked", user_id=user1.id
    )
    crud.like_tweet(db_session, user_id=user2.id, tweet_id=tweet.id)
    response = client.delete(
        f"/api/tweets/{tweet.id}/likes", headers={"api-key": user2.api_key}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True


def test_follow_user(client: TestClient, db_session: Session, create_test_users):
    user1, user2 = create_test_users
    response = client.post(
        f"/api/users/{user2.id}/follow", headers={"api-key": user1.api_key}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True


def test_unfollow_user(client: TestClient, db_session: Session, create_test_users):
    user1, user2 = create_test_users
    crud.follow_user(db_session, user_id=user1.id, follow_id=user2.id)
    response = client.delete(
        f"/api/users/{user2.id}/follow", headers={"api-key": user1.api_key}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True


def test_get_tweets(client: TestClient, db_session: Session, create_test_users):
    user1, _ = create_test_users
    crud.create_tweet(db_session, tweet="Test tweet for feed", user_id=user1.id)
    response = client.get("/api/tweets", headers={"api-key": user1.api_key})
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert "tweets" in data


def test_get_tweets_no_api_key(client: TestClient):
    response = client.get("/api/tweets")
    assert response.status_code == 400
    assert response.json()["error_message"] == "API Key is required"


def test_get_my_profile(client: TestClient, db_session: Session, create_test_users):
    user1, _ = create_test_users
    response = client.get("/api/users/me", headers={"api-key": user1.api_key})
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert "user" in data
    assert data["user"]["id"] == user1.id


def test_get_my_profile_no_api_key(client: TestClient):
    response = client.get("/api/users/me")
    assert response.status_code == 400
    assert response.json()["error_message"] == "API Key is required"


def test_get_my_profile_invalid_api_key(client: TestClient):
    invalid_api_key = "invalid_key"
    response = client.get("/api/users/me", headers={"api-key": invalid_api_key})
    assert response.status_code == 400
    assert response.json()["error_message"] == "Invalid API Key"


def test_get_user_profile(client: TestClient, db_session: Session, create_test_users):
    user1, _ = create_test_users
    response = client.get(f"/api/users/{user1.id}")
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data["result"] is True
    assert "user" in data
    assert data["user"]["id"] == user1.id


def test_get_user_profile_no_api_key(client: TestClient):
    response = client.get("/api/users/1")
    assert response.status_code == 404
    assert response.json()["error_message"] == "User not found"


def test_get_user_profile_nonexistent(client: TestClient, create_test_users):
    user1, _ = create_test_users
    response = client.get("/api/users/99999", headers={"api-key": user1.api_key})
    assert response.status_code == 404
    assert response.json()["error_message"] == "User not found"
