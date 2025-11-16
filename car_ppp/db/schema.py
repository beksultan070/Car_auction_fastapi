from pydantic import BaseModel
from .models import UserRole, FuelType, TRANSMISSION, STATUS


class UserProfileSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    age: int
    email: str
    role: UserRole
    password: str


class BrandSchema(BaseModel):
    brand_name: str


class ModelSchema(BaseModel):
    model_name: str
    brand_id: int


class CarSchema(BaseModel):
    year: int
    mileage: int
    image: str
    fuel_type: FuelType
    transmission: TRANSMISSION
    seller_id: int


class AuctionSchema(BaseModel):
    start_price: int
    min_price: int
    status: STATUS
    car_id: int


class ReviewSchema(BaseModel):
    comment: str
    user_id: int




