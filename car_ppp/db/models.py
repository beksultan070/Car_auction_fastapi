from .database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Date, Enum, Text, ForeignKey, DateTime
from datetime import datetime, date
from enum import Enum as PyEnum
from typing import List




class UserRole(str, PyEnum):
    seller = 'seller'
    buyer = 'buyer'


class FuelType(str,PyEnum):
    electro = 'electro'
    gas = 'gas'
    petrol = 'petrol'
    hybrid = 'hybrid'


class TRANSMISSION(str, PyEnum):
    auto = 'auto'
    manual = 'manual'


class STATUS(str, PyEnum):
    active = 'active'
    cancelled= 'cancelled'
    end = 'end'





class UserProfile(Base):
    __tablename__ = 'userprofile'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    username: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    age: Mapped[int] = mapped_column(Integer)
    email: Mapped[str] = mapped_column(String, unique=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.seller, nullable=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    password: Mapped[str] = mapped_column(String, nullable=False)

    car_seller: Mapped[List['Car']] = relationship('Car', back_populates='seller', cascade='all,delete-orphan')
    review: Mapped[List['Review']] = relationship('Review', back_populates='user', cascade='all,delete-orphan')


class Brand(Base):
    __tablename__ = 'brand'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    brand_name: Mapped[str] = mapped_column(String(32), unique=True)

    model: Mapped[List['Model']] = relationship('Model', back_populates='brand', cascade='all, delete-orphan')


class Model(Base):
    __tablename__ = 'model'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    model_name: Mapped[str] = mapped_column(String(32), unique=True)

    brand_id: Mapped[int] = mapped_column(ForeignKey('brand.id'))
    brand: Mapped['Brand'] = relationship('Brand', back_populates='model')


class Car(Base):
    __tablename__ = 'car'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    year: Mapped[int] = mapped_column(Integer)
    mileage: Mapped[int] = mapped_column(Integer, default=0)
    image: Mapped[str] = mapped_column(String)
    fuel_type : Mapped[FuelType] = mapped_column(Enum(FuelType))
    transmission: Mapped[TRANSMISSION] = mapped_column(Enum(TRANSMISSION))

    seller_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    seller: Mapped['UserProfile'] = relationship('UserProfile', back_populates='car_seller')

    auction: Mapped[List['Auction']] = relationship('Auction', back_populates='car', cascade='all, delete-orphan')



class Auction(Base):
    __tablename__ = 'auction'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    start_price: Mapped[int] = mapped_column(Integer)
    min_price: Mapped[int] = mapped_column(Integer, nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime]  =mapped_column(DateTime)
    status: Mapped[STATUS] = mapped_column(Enum(STATUS), default=STATUS.active)


    car_id: Mapped[int] = mapped_column(Integer, ForeignKey('car.id'), unique=True)
    car: Mapped['Car'] = relationship('Car', back_populates='auction')


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    comment: Mapped[str] = mapped_column(Text)


    user_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='review')




