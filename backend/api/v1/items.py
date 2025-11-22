from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...config.database import get_db
from ...services import item_service

router = APIRouter()

@router.get('/')
async def read_items(db: Session = Depends(get_db)):
    '''Get all clothing items'''
    return item_service.get_items(db)

@router.get('/{item_id}')
async def read_item(item_id: int, db: Session = Depends(get_db)):
    '''Get a specific clothing item by ID'''
    item = item_service.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')
    return item

@router.post('/')
async def create_new_item(item: dict, db: Session = Depends(get_db)):
    '''Create a new clothing item'''
    return item_service.create_item(db, item)

@router.put('/{item_id}')
async def update_existing_item(item_id: int, item: dict, db: Session = Depends(get_db)):
    '''Update an existing clothing item'''
    updated_item = item_service.update_item(db, item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail='Item not found')
    return updated_item

@router.delete('/{item_id}')
async def delete_item_endpoint(item_id: int, db: Session = Depends(get_db)):
    '''Delete a clothing item by ID'''
    deleted = item_service.delete_item(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Item not found')
    return {'message': 'Item deleted successfully'}
