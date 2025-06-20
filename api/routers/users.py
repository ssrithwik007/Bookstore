from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from typing import List
from passlib.context import CryptContext

router = APIRouter(
    prefix="/users"
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def validate_user(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

def validate_book(book_id: int, db: Session):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

@router.get("/{user_id}", response_model=schemas.UserOut, status_code=status.HTTP_200_OK, tags=["Users"])
def get_user(user_id: int, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/", response_model=List[schemas.UserOut], status_code=status.HTTP_200_OK, tags=["Users"])
def get_all_users(db: Session=Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.post("/", status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(request: schemas.UserCreate, db: Session=Depends(get_db)):
    hashed_pwd = pwd_context.hash(request.password)
    new_user = models.User(
        username = request.username,
        email = request.email,
        password = hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"User created successfully"}

@router.delete("/{user_id}", status_code=status.HTTP_200_OK, tags=["Users"])
def delete_user(user_id: int, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).delete(synchronize_session=False)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.commit()
    return {"User Removed Successfully"}

@router.put("/{user_id}", status_code=status.HTTP_200_OK, tags=["Users"])
def update_user(user_id: int, request: schemas.UserCreate, db: Session=Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == user_id)
    user = user_query.first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user_data = request.model_dump()

    if "password" in user_data and user_data["password"]:
        user_data["password"] = pwd_context.hash(user_data["password"])

    user_query.update(user_data, synchronize_session=False)
    db.commit()

    db.commit()
    return {"User successfully updated"}

@router.get("/{user_id}/cart", response_model=List[schemas.CartOut], status_code=status.HTTP_200_OK, tags=["Cart"])
def get_cart(user_id: int, db: Session=Depends(get_db)):
    try:
        validate_user(user_id, db)
    except Exception as e:
        raise e

    cart = db.query(models.Cart).filter(models.Cart.user_id == user_id).all()

    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart is empty") 
    
    return cart

@router.post("/{user_id}/cart", response_model=schemas.CartOut, status_code=status.HTTP_201_CREATED, tags=["Cart"])
def add_to_cart(user_id: int, request: schemas.CartItem, db: Session=Depends(get_db)):
    try:
        validate_book(request.book_id, db)
        validate_user(user_id, db)
    except Exception as e:
        raise e

    cart_item = db.query(models.Cart).filter(models.Cart.user_id == user_id,
                                                 models.Cart.book_id == request.book_id).first()
    if cart_item:
        cart_item.quantity += request.quantity
        db.commit()
        db.refresh(cart_item)
        return cart_item
    
    new_cart_item = models.Cart(
        user_id = user_id,
        book_id = request.book_id,
        quantity = request.quantity
    )

    db.add(new_cart_item)
    db.commit()
    db.refresh(new_cart_item)

    return new_cart_item

@router.delete("/{user_id}/cart", status_code=status.HTTP_200_OK, tags=["Cart"])
def remove_from_cart(user_id: int, request: schemas.CartItem, db: Session=Depends(get_db)):
    try:
        validate_book(request.book_id, db)
        validate_user(user_id, db)
    except Exception as e:
        raise e
    
    cart_item = db.query(models.Cart).filter(models.Cart.user_id == user_id,
                                             models.Cart.book_id == request.book_id).first()
    
    if not cart_item or cart_item.quantity == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book does not exist in cart")
    
    if cart_item.quantity - request.quantity > 0:
        cart_item.quantity -= request.quantity
        db.commit()
        db.refresh(cart_item)
        return cart_item
    else:
        db.delete(cart_item)
        db.commit()
        return {"Removed item from cart successfully"}
    
@router.delete("/{user_id}/cart/clear", status_code=status.HTTP_200_OK, tags=["Cart"])
def clear_cart(user_id: int, db: Session=Depends(get_db)):
    try:
        validate_user(user_id, db)
    except Exception as e:
        raise e
    
    cart = db.query(models.Cart).filter(models.Cart.user_id == user_id).all()

    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart is empty")

    db.query(models.Cart).filter(models.Cart.user_id == user_id).delete(synchronize_session=False)
    db.commit()

    return {"message": "Cart Cleared"}
    
@router.get("/{user_id}/purchases", response_model= List[schemas.PurchaseOut], status_code=status.HTTP_200_OK, tags=["Purchase"])
def get_all_purchases(user_id: int, db: Session=Depends(get_db)):
    try:
        validate_user(user_id, db)
    except Exception as e:
        raise e
        
    purchases = db.query(models.Purchase).filter(models.Purchase.user_id == user_id).all()

    if not purchases:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No purchase history found")
        
    return purchases
    
@router.post("/{user_id}/purchases", status_code=status.HTTP_201_CREATED, tags=["Purchase"])
def purchase_book(user_id: int, request: schemas.PurchaseCreate, db: Session=Depends(get_db)):
    try:
        validate_book(request.book_id, db)
        validate_user(user_id, db)
    except Exception as e:
        raise e

    new_purchase=models.Purchase(
        user_id = user_id,
        book_id = request.book_id,
        quantity = request.quantity
    )

    db.add(new_purchase)
    db.commit()
    db.refresh(new_purchase)

    return {"message": "Purchase successful",
            "Purchase id": new_purchase.id}

@router.post("/{user_id}/checkout", status_code=status.HTTP_201_CREATED, tags=["Purchase", "Cart"])
def checkout_cart(user_id: int, db: Session=Depends(get_db)):
    try:
        validate_user(user_id, db)
    except Exception as e:
        raise e
    
    cart = db.query(models.Cart).filter(models.Cart.user_id == user_id).all()

    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart is empty")
    
    for item in cart:
        new_purchase = models.Purchase(
            user_id = item.user_id,
            book_id = item.book_id,
            quantity = item.quantity
        )
        db.add(new_purchase)
        db.commit()
        db.refresh(new_purchase)

    db.query(models.Cart).filter(models.Cart.user_id == user_id).delete(synchronize_session=False)
    db.commit()

    return {"message": "Purchase Successful"}

@router.delete("/{user_id}/purchases/{book_id}", status_code=status.HTTP_201_CREATED, tags=["Purchase"])
def refund_book(user_id: int, book_id: int, db: Session=Depends(get_db)):
    try:
        validate_book(book_id, db)
        validate_user(user_id, db)
    except Exception as e:
        raise e
    
    purchase = db.query(models.Purchase).filter(models.Purchase.user_id == user_id,
                                                models.Purchase.book_id == book_id).first()
    
    if purchase:
        db.delete(purchase)
        db.commit()
        return {"message": "Refund successful"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Purchase doesn't exist"})