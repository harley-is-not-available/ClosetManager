from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...config.database import get_db
from ...services import upload_service

router = APIRouter()

@router.post('/')
async def upload_item_image(file: object, db: Session = Depends(get_db)):
    '''Upload an image for a clothing item'''
    return upload_service.upload_image(db, file)
