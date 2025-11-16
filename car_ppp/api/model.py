from fastapi import APIRouter, Depends, HTTPException, status
from car_ppp.db.schema import ModelSchema
from car_ppp.db.models import Model
from car_ppp.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

model_router = APIRouter(prefix='/model', tags=['Model'])



@model_router.post('/create')
async def create_model(model_data: ModelSchema, db: Session = Depends(get_db)):
    model_db = Model(**model_data.dict())
    db.add(model_db)
    db.commit()
    db.refresh(model_db)
    return {'answer db': 'success created'}


@model_router.get('/get_list', response_model=List[ModelSchema])
async def list_model(db: Session = Depends(get_db)):
    model_db = db.query(Model).all()
    return model_db



@model_router.get('/get_detail', response_model=ModelSchema)
async def detail_model(model_id: int, db: Session = Depends(get_db)):
    model_db = db.query(Model).filter(Model.id == model_id).first()
    if model_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday maalymat jok')
    return model_db


@model_router.put('/update', response_model=ModelSchema)
async def update_model(model_id: int, model_data: ModelSchema, db: Session = Depends(get_db)):
    model_db = db.query(Model).filter(Model.id == model_id).first()
    if model_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday maalymat tabylgan jok')
    model_db.model_name = model_data.model_name
    db.commit()
    db.refresh(model_db)
    return model_db



@model_router.delete('/delete')
async def delete_model(model_id, db: Session = Depends(get_db)):
    model_db = db.query(Model).filter(Model.id == model_id).first()
    if model_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday maalymat jok')
    db.delete(model_db)
    db.commit()
    return {'answer db': 'success deleted'}
