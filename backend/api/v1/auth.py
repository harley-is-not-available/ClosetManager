from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...config.database import get_db
from ...services import auth_service

router = APIRouter()

@router.post('/register')
async def register(user: dict, db: Session = Depends(get_db)):
    '''Register a new user'''
    return auth_service.create_user(db, user)

@router.post('/login')
async def login(form_data: dict, db: Session = Depends(get_db)):
    '''Login user and return access token'''
    token = auth_service.authenticate_user(db, form_data)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return token
