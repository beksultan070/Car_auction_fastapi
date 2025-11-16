from fastapi import APIRouter,HTTPException,Depends,status
from car_ppp.db.schema import AuctionSchema
from car_ppp.db.database import SessionLocal
from car_ppp.db.models import Auction
from typing import List
from sqlalchemy.orm import Session

async def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


auction_router=APIRouter(prefix='/auction',tags=['Auction'])


@auction_router.post('/create')
async def create_auction(auction_data:AuctionSchema,db:Session=Depends(get_db)):
    auction_db=Auction(**auction_data.dict())
    db.add(auction_db)
    db.commit()
    db.refresh(auction_db)
    return auction_db

@auction_router.get('/get_list',response_model=List[AuctionSchema])
async def list_auction(db:Session=Depends(get_db)):
    auction_db=db.query(Auction).all()
    return auction_db

@auction_router.get('/get_detail',response_model=AuctionSchema)
async def detail_auction(auction_id:int,db:Session=Depends(get_db)):
    auction_db=db.query(Auction).filter(Auction.id==auction_id).first()
    if auction_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    return auction_db

@auction_router.put('/update',response_model=AuctionSchema)
async def update_auction(auction_id,auction_data:AuctionSchema,db:Session=Depends(get_db)):
    auction_db=db.query(Auction).filter(Auction.id==auction_id).first()
    if auction_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    for auction_key,auction_value in auction_data.dict().items():
        setattr(auction_db,auction_key,auction_value)
    db.commit()
    db.refresh(auction_db)
    return auction_db

@auction_router.delete('/delete')
async def delete_auction(auction_id:int,db:Session=Depends(get_db)):
    auction_db=db.query(Auction).filter(Auction.id==auction_id).first()
    if auction_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    db.delete(auction_db)
    db.commit()
    return {'answer db':'success deleted'}