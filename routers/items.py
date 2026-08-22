from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload

import database
import models
import schemas
import security

router = APIRouter(
    prefix="/items",
    tags=["items"],
)


# 自分のアイテム一覧取得（認証必須）
@router.get("/", response_model=list[schemas.ItemResponse])
def get_items(
    skip: int = Query(0, ge=0, description="取得開始位置"),
    limit: int = Query(20, ge=1, le=100, description="1回の取得上限件数"),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    # 本人の items のみ取得（N+1対策 & ページネーション）
    return (
        db.query(models.ItemModel)
        .options(joinedload(models.ItemModel.owner))
        .filter(models.ItemModel.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


# 自分のアイテム1件取得（認証必須）
@router.get("/{item_id}", response_model=schemas.ItemResponse)
def get_item(
    item_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    # ID と user_id の両方で絞り込み（他人のデータなら見つからない扱いにする）
    item = (
        db.query(models.ItemModel)
        .filter(
            models.ItemModel.id == item_id,
            models.ItemModel.user_id == current_user.id,
        )
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# 新規作成（認証必須）
@router.post(
    "/",
    response_model=schemas.ItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    new_item = models.ItemModel(**item.model_dump(), user_id=current_user.id)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


# 更新（認証必須）
@router.put("/{item_id}", response_model=schemas.ItemResponse)
def update_item(
    item_id: int,
    updated_item: schemas.ItemCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    item_query = db.query(models.ItemModel).filter(
        models.ItemModel.id == item_id,
        models.ItemModel.user_id == current_user.id,
    )
    item = item_query.first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item_query.update(updated_item.model_dump(), synchronize_session=False)
    db.commit()
    return item_query.first()


# 削除（認証必須）
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    item_query = db.query(models.ItemModel).filter(
        models.ItemModel.id == item_id,
        models.ItemModel.user_id == current_user.id,
    )
    if not item_query.first():
        raise HTTPException(status_code=404, detail="Item not found")

    item_query.delete(synchronize_session=False)
    db.commit()
    return