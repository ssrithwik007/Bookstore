from typing import List, Optional
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

class BookUpdate(BaseModel):
    name : Optional[str] = None
    author : Optional[str] = None
    description : Optional[str] = None
    genre : Optional[str] = None
    price : Optional[float] = None      

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: Optional[str] = "user"

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

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
    role: str
    cart_items: List[CartOut]
    purchases: List[PurchaseOut]

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[str] = None