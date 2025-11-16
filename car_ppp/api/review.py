from fastapi import APIRouter,HTTPException,Depends,status
from car_ppp.db.schema import ReviewSchema
from car_ppp.db.database import SessionLocal
from car_ppp.db.models import Review
from sqlalchemy.orm import Session
from typing import List


async  def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


review_router=APIRouter(prefix='/review',tags=['Review'])

@review_router.post('/create')
async def create_review(review_data:ReviewSchema,db:Session=Depends(get_db)):
    review_db=Review(**review_data.dict())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db

@review_router.get('/get_list',response_model=List[ReviewSchema])
async def list_review(db:Session=Depends(get_db)):
    review_db=db.query(Review).all()
    return review_db

@review_router.get('/detail_review',response_model=ReviewSchema)
async def detail_review(review_id:int,db:Session=Depends(get_db)):
    review_db=db.query(Review).filter(Review.id==review_id).first()
    if review_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    return review_db

@review_router.put('/update',response_model=ReviewSchema)
async def update_review(review_id:int,review_data:ReviewSchema,db:Session=Depends(get_db)):
    review_db=db.query(Review).filter(Review.id==review_id).first()
    if review_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    for review_key,review_value in review_data.dict().items():
        setattr(review_db,review_key,review_value)
    db.commit()
    db.refresh(review_db)
    return review_db


@review_router.delete('/delete')
async def delete_review(review_id:int,db:Session=Depends(get_db)):
    review_db=db.query(Review).filter(Review.id==review_id).first()
    if review_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    db.delete(review_db)
    db.commit()
    return {'answer':'success deleted'}