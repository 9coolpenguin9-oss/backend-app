from pydantic import BaseModel, ConfigDict, EmailStr


# 入力（リクエストボディ）用スキーマ
class ItemCreate(BaseModel):
    name: str


# 出力（レスポンス）用スキーマ（必要に応じて追加）
class ItemResponse(BaseModel):
    id: int
    name: str
    user_id: int

    ConfigDict(from_attributes=True)


# ユーザー登録時に受け取るデータ
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# 外部へ返却するデータ（パスワード情報は除外）
class UserResponse(BaseModel):
    id: int
    email: str
    items: list[ItemResponse] = []

    # ORMモデルからPydanticモデルへの変換を許可
    model_config = ConfigDict(from_attributes=True)
