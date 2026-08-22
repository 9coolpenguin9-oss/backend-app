from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from core.config import settings

# DBエンジン（接続ポイント）の作成（core/config.py から DATABASE_URL を取得）
engine = create_engine(settings.DATABASE_URL)

# DB操作用セッションの生成工場
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# SQLAlchemyモデルの基底クラス
class Base(DeclarativeBase):
    pass


# リクエストごとにDBセッションを生成・切断するジェネレータ
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()