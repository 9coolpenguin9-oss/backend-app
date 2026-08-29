from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import APIRouter
import database

router = APIRouter(
    tags=["System"],
)

@router.get("/health")
def health_check(db: Session = Depends(database.get_db)):
    try:
        # DBに軽いクエリを投げて接続確認
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        # DBが落ちている場合はエラーなどを返す
        return {"status": "error", "database": str(e)}