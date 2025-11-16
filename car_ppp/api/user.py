from fastapi import APIRouter, Depends, HTTPException, status
from car_ppp.db.models import UserProfile
from car_ppp.db.schema import UserProfileSchema
from car_ppp.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


user_router = APIRouter(prefix='/user', tags=['UserProfile'])

@user_router.post('/create')
async def create_user(user_data: UserProfileSchema, db: Session = Depends(get_db)):
    user_db = UserProfile(**user_data.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db



@user_router.put('/update', response_model=UserProfileSchema)
async def update_user(user_id, user_data: UserProfileSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday maalymat jok')
    for user_key, user_value in user_data.dict().items():
        setattr(user_db, user_key, user_value)
    db.commit()
    db.refresh(user_db)
    return user_db


@user_router.get('/list_user', response_model=List[UserProfileSchema])
async def list_user(db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).all()
    return user_db

@user_router.get('/detail_user', response_model=UserProfileSchema)
async def detail_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Myndady adam tabylgan jok')
    return user_db


@user_router.delete('/delete')
async def delete_user(user_id, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday maalymat jok')
    db.delete(user_db)
    db.commit()
    return {'answer db': 'success deleted'}
