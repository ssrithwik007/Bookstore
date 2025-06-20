from typing import List
from pydantic import BaseModel

class BookCreate(BaseModel):
    name : str
    author : str
    description : str
    genre : str
    price : float

class BookOut(BookCreate):
    id: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    passwrod: str

class CartItem(BaseModel):
    book_id: int
    quantity: int = 1

class CartOut(BaseModel):
    id: int
    quantity: int
    book: BookOut

    class Config:
        orm_mode = True

class PurchaseCreate(BaseModel):
    book_id: int
    quantity: int = 1

class PurchaseOut(BaseModel):
    id: int
    quantity: int
    book: BookOut

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    cart_items: List[CartOut]
    purchases: List[PurchaseOut]

    class Config:
        orm_mode = True