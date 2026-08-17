from database import Base
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


# 実際のDBテーブル "items" に対応するSQLAlchemyモデル
class ItemModel(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)

    # ① 外部キー（users テーブルの id を参照）
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # ② User オブジェクトへの参照
    owner: Mapped["User"] = relationship(back_populates="items")


# ユーザーテーブルクラス
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    # ③ 1人のユーザーが所持する ItemModel のリスト参照
    items: Mapped[list["ItemModel"]] = relationship(back_populates="owner")