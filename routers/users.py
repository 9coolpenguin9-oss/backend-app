from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import database, models, schemas, security

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # メールアドレスの重複チェック
    db_user = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # パスワードのハッシュ化
    hashed_password = security.get_password_hash(user.password)

    # DBへ保存
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ログイン処理
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    # 1. ユーザーの存在確認
    user = (
        db.query(models.User)
        .filter(models.User.email == form_data.username)
        .first()
    )

    # 2. 認証チェック
    if not user or not security.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. トークン発行
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# --- 自分の情報取得（保護されたエンドポイント） ---
@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(security.get_current_user)):
    return current_user