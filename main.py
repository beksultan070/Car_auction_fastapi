from fastapi import FastAPI
from car_ppp.api import user
import uvicorn


car_ppp = FastAPI(title='Online Shop')



car_ppp.include_router(user.user_router)




if __name__ == '__main__':
    uvicorn.run(car_ppp, host='127.0.0.1', port=8003)