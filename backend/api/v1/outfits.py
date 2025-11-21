from typing import List, Optional
from uuid import UUID

from app.config.database import get_db
from app.models.outfit import (
    Outfit,
    OutfitCreate,
    OutfitUpdate,
)
from app.services.outfit_service import (
    create_outfit,
    delete_outfit,
    get_outfit,
    get_outfits,
    update_outfit,
)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/outfits", response_model=List[Outfit])
async def read_outfits(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    outfits = get_outfits(db, skip=skip, limit=limit)
    return outfits


@router.get("/outfits/{outfit_id}", response_model=Outfit)
async def read_outfit(outfit_id: UUID, db: Session = Depends(get_db)):
    db_outfit = get_outfit(db, outfit_id=outfit_id)
    if db_outfit is None:
        raise HTTPException(status_code=404, detail="Outfit not found")
    return db_outfit


@router.post("/outfits", response_model=Outfit)
async def create_new_outfit(
    outfit: OutfitCreate, db: Session = Depends(get_db)
):
    return create_outfit(db, outfit)


@router.put("/outfits/{outfit_id}", response_model=Outfit)
async def update_existing_outfit(
    outfit_id: UUID, outfit: OutfitUpdate, db: Session = Depends(get_db)
):
    db_outfit = get_outfit(db, outfit_id=outfit_id)
    if db_outfit is None:
        raise HTTPException(status_code=404, detail="Outfit not found")
    return update_outfit(db, db_outfit, outfit)


@router.delete("/outfits/{outfit_id}")
async def delete_outfit_endpoint(
    outfit_id: UUID, db: Session = Depends(get_db)
):
    db_outfit = get_outfit(db, outfit_id=outfit_id)
    if db_outfit is None:
        raise HTTPException(status_code=404, detail="Outfit not found")
    delete_outfit(db, outfit_id)
    return {"message": "Outfit deleted successfully"}
