from fastapi import APIRouter, Depends, HTTPException, status
from car_ppp.db.schema import BrandSchema
from car_ppp.db.models import Brand
from car_ppp.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

brand_router = APIRouter(prefix='/brand', tags=['Brand'])



@brand_router.post('/create')
async def create_brand(brand_data: BrandSchema, db: Session = Depends(get_db)):
    brand_db = Brand(brand_name=brand_data.brand_name)
    db.add(brand_db)
    db.commit()
    db.refresh(brand_db)
    return {'answer db': 'success created'}


@brand_router.get('/get_list', response_model=List[BrandSchema])
async def list_brand(db: Session = Depends(get_db)):
    brand_db = db.query(Brand).all()
    return brand_db



@brand_router.get('/get_detail', response_model=BrandSchema)
async def detail_brand(brand_id: int, db: Session = Depends(get_db)):
    brand_db = db.query(Brand).filter(Brand.id == brand_id).first()
    if brand_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday maalymat jok')
    return brand_db


@brand_router.put('/update', response_model=BrandSchema)
async def update_brand(brand_id: int, brand_data: BrandSchema, db: Session = Depends(get_db)):
    brand_db = db.query(Brand).filter(Brand.id == brand_id).first()
    if brand_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday maalymat tabylgan jok')
    brand_db.brand_name=brand_data.brand_name
    db.commit()
    db.refresh(brand_db)
    return brand_db



@brand_router.delete('/delete')
async def delete_brand(brand_id, db: Session = Depends(get_db)):
    brand_db = db.query(Brand).filter(Brand.id == brand_id).first()
    if brand_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday maalymat jok')
    db.delete(brand_db)
    db.commit()
    return {'answer db': 'success deleted'}
