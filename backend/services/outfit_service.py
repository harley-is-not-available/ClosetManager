from uuid import UUID

from app.models.outfit import (
    Outfit,
    OutfitCreate,
    OutfitUpdate,
)
from sqlalchemy.orm import Session


def get_outfits(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Outfit).offset(skip).limit(limit).all()


def get_outfit(db: Session, outfit_id: UUID):
    return db.query(Outfit).filter(Outfit.id == outfit_id).first()


def create_outfit(db: Session, outfit: OutfitCreate):
    db_outfit = Outfit(**outfit.dict())
    db.add(db_outfit)
    db.commit()
    db.refresh(db_outfit)
    return db_outfit


def update_outfit(db: Session, db_outfit: Outfit, outfit: OutfitUpdate):
    update_data = outfit.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_outfit, key, value)
    db.commit()
    db.refresh(db_outfit)
    return db_outfit


def delete_outfit(db: Session, outfit_id: UUID):
    db.query(Outfit).filter(Outfit.id == outfit_id).delete()
    db.commit()
