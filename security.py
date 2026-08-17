from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import bcrypt
from sqlalchemy.orm import Session

import database
import models


# --- JWTの設定値 ---
SECRET_KEY = "your-secret-key-keep-it-secret"  # 署名用の秘密鍵
ALGORITHM = "HS256"  # 暗号化アルゴリズム
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # トークンの有効期限（30分）

# Swagger UIの「Authorize」ボタンとログイン処理のURLを紐付ける設定
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


# 1. ハッシュ化する関数（72バイト制限の安全対策付き）
def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode("utf-8")[:72]  # 72バイトで安全に切り捨て
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


# 2. パスワード検証関数（72バイト制限の安全対策付き）
def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password.encode("utf-8")[:72]
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)


# 3. アクセストークン発行関数（ログイン用）
def create_access_token(data: dict) -> str:
    """ユーザー識別情報と有効期限を組み込んだJWTトークンを生成"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 4. トークンを検証してユーザー情報を取得する関数
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # トークンを解読（デコード）してメールアドレスを取得
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # DBから対象のユーザーを取得
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user