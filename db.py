from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Boolean, DateTime, event
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from datetime import datetime

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


class Users(UserMixin,db.Model):
    __tablename__='users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250),nullable=False)
    email: Mapped[str] = mapped_column(String(250),nullable=False)
    password: Mapped[str] = mapped_column(String(1000),nullable=False)
    created_on: Mapped[datetime] = mapped_column(DateTime,nullable=False,server_default=func.now())
    confirmed: Mapped[bool] = mapped_column(Boolean,nullable=False,default=False)
    confirmed_on: Mapped[datetime] = mapped_column(DateTime,nullable=True)

    def __str__(self) -> str:
        return f"User ID: {self.id}, Name: {self.name}"
    
@event.listens_for(Users.password,'set',retval=True)
def hash_user_password(target,value,oldvalue,initiator):
    if value!=oldvalue:
        return generate_password_hash(value,method='scrypt:32768:8:1')
    return value



class Fragrances(db.Model):
    __tablename__='fragrances'
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    name: Mapped[str] = mapped_column(String(250),nullable=False)
    img_url: Mapped[str] = mapped_column(String(500),nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    brand: Mapped[str] = mapped_column(String(250), nullable=False)
    price: Mapped[str] = mapped_column(String(250),nullable=False)
    quantity: Mapped[int] = mapped_column(Integer,nullable=False)
