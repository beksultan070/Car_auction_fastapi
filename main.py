from fastapi import FastAPI
from car_ppp.api import user, brand, model, car, auction, review
import uvicorn


car_ppp = FastAPI(title='Online Shop')


car_ppp.include_router(brand.brand_router)
car_ppp.include_router(user.user_router)
car_ppp.include_router(model.model_router)
car_ppp.include_router(car.car_router)
car_ppp.include_router(auction.auction_router)
car_ppp.include_router(review.review_router)




if __name__ == '__main__':
    uvicorn.run(car_ppp, host='127.0.0.1', port=8003)