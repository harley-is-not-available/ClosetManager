from uuid import UUID

from app.models.collection import (
    Collection,
    CollectionCreate,
    CollectionUpdate,
)
from sqlalchemy.orm import Session


def get_collections(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Collection).offset(skip).limit(limit).all()


def get_collection(db: Session, collection_id: UUID):
    return db.query(Collection).filter(Collection.id == collection_id).first()


def create_collection(db: Session, collection: CollectionCreate):
    db_collection = Collection(**collection.dict())
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return db_collection


def update_collection(db: Session, db_collection: Collection, collection: CollectionUpdate):
    update_data = collection.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_collection, key, value)
    db.commit()
    db.refresh(db_collection)
    return db_collection


def delete_collection(db: Session, collection_id: UUID):
    db.query(Collection).filter(Collection.id == collection_id).delete()
    db.commit()
