import pytest

# ルートエンドポイントのテスト
def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200

# ログイン成功テスト
def test_login_success(client):
    # テスト用のサンプルユーザーを作成（テスト終了時に自動ロールバック）
    client.post(
        "/users/",
        json={"email": "test@example.com", "password": "correctpassword"}
    )

    response = client.post(
        "/users/login",
        data={"username": "test@example.com", "password": "correctpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

# 存在しないユーザーでのログイン失敗テスト
def test_login_user_not_found(client):
    response = client.post(
        "/users/login",
        data={"username": "test@nonexistent_user.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401

# トークンなしでのアイテム取得失敗テスト（401）
def test_get_items_unauthorized(client):
    response = client.get("/items/")
    assert response.status_code == 401

# トークン付きでのアイテム取得成功テスト（200）
def test_get_items_authorized(client):
    # テスト用のサンプルユーザーを作成（テスト終了時に自動ロールバック）
    client.post(
        "/users/",
        json={"email": "test@example.com", "password": "correctpassword"}
    )

    # ログインしてトークンを取得
    login_res = client.post(
        "/users/login",
        data={"username": "test@example.com", "password": "correctpassword"},
    )
    token = login_res.json()["access_token"]

    # Authorization ヘッダーに Bearer トークンをセットしてアクセス
    response = client.get(
        "/items/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # 返り値がリスト形式であることを確認

def test_read_main(client):
    response = client.get("/health")
    assert response.status_code == 200