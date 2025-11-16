from fastapi import APIRouter,HTTPException,Depends,status
from car_ppp.db.schema import CarSchema
from car_ppp.db.database import SessionLocal
from car_ppp.db.models import Car
from sqlalchemy.orm import Session
from typing import List


async def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

car_router=APIRouter(prefix='/car',tags=['Car'])


@car_router.post('/create')
async def create_car(car_data:CarSchema,db:Session=Depends(get_db)):
    car_db=Car(**car_data.dict())
    db.add(car_db)
    db.commit()
    db.refresh(car_db)
    return car_db

@car_router.get('/get_list',response_model=List[CarSchema])
async def list_car(db:Session=Depends(get_db)):
    car_db=db.query(Car).all()
    return car_db

@car_router.get('/get_detail',response_model=CarSchema)
async def detail_car(car_id:int,db:Session=Depends(get_db)):
    car_db=db.query(Car).filter(Car.id==car_id).first()
    if car_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    return car_db

@car_router.put('/update',response_model=CarSchema)
async def update_car(car_id:int,car_data:CarSchema,db:Session=Depends(get_db)):
    car_db=db.query(Car).filter(Car.id==car_id).first()
    if car_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    for car_key,car_value in car_data.dict().items():
        setattr(car_db,car_key,car_value)
    db.commit()
    db.refresh(car_db)
    return car_db

@car_router.delete('/delete')
async def delete_car(car_id:int,db:Session=Depends(get_db)):
    car_db=db.query(Car).filter(Car.id==car_id).first()
    if car_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    db.delete(car_db)
    db.commit()
    return {'answer db':'success deleted'}