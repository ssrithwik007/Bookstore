from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import schemas, models
from ..database import get_db
from typing import List
from passlib.context import CryptContext
from .login import admin_only, user_only, trail_admin_nd_user

router = APIRouter(
    prefix="/users"
    )

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def init_admin(username: str, password: str):
    db =  next(get_db())

    existing_admin = db.query(models.User).filter(models.User.username == username).first()
    if not existing_admin:
        hashed_pwd = pwd_context.hash(password)
        new_admin = models.User(
            username = username,
            email = "admin-doesn't-need-email",
            password = hashed_pwd,
            role = "admin"
        )

        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)

def validate_user(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

def validate_book(book_id: int, db: Session):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

@router.get("/", response_model=List[schemas.UserOut], status_code=status.HTTP_200_OK, tags=["Users"])
def get_all_users(db: Session=Depends(get_db), current_user: schemas.TokenData=Depends(admin_only)):
    users = db.query(models.User).all()
    return users

@router.get("/me", response_model=schemas.UserOut, status_code=status.HTTP_200_OK, tags=["Users"])
def get_account(db: Session=Depends(get_db), current_user: schemas.TokenData=Depends(trail_admin_nd_user)):
    user = db.query(models.User).filter(models.User.id == current_user.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.post("/", status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_account(request: schemas.UserCreate, db: Session=Depends(get_db)):

    existing_username = db.query(models.User).filter((models.User.username == request.username)).first()

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken"
            )
    
    existing_email = db.query(models.User).filter((models.User.email == request.email)).first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already used"
        )

    hashed_pwd = pwd_context.hash(request.password)
    new_user = models.User(
        username = request.username,
        email = request.email,
        password = hashed_pwd,
        role = request.role
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User created successfully"}
    
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists"
        )

@router.delete("/me", status_code=status.HTTP_200_OK, tags=["Users"])
def delete_account(db: Session=Depends(get_db), current_user: schemas.TokenData=Depends(trail_admin_nd_user)):
    user = db.query(models.User).filter(models.User.id == current_user.user_id).delete(synchronize_session=False)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.commit()
    return {"message": "User Removed Successfully"}

@router.put("/me", status_code=status.HTTP_200_OK, tags=["Users"])
def update_details(request: schemas.UserUpdate, db: Session=Depends(get_db), current_user: schemas.TokenData=Depends(trail_admin_nd_user)):

    existing_email = db.query(models.User).filter(models.User.email == request.email,
                                                   models.User.id != current_user.user_id).first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already used"
        )

    existing_username = db.query(models.User).filter(models.User.username == request.username,
                                                      models.User.id != current_user.user_id).first()

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken"
            )

    user_query = db.query(models.User).filter(models.User.id == current_user.user_id)
    user = user_query.first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user_data = request.model_dump(exclude_unset=True)

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update"
        )

    if "password" in user_data and user_data["password"]:
        user_data["password"] = pwd_context.hash(user_data["password"])

    user_query.update(user_data, synchronize_session=False)
    db.commit()

    db.commit()
    return {"message": "User successfully updated"}

@router.get("/me/cart", response_model=List[schemas.CartOut], status_code=status.HTTP_200_OK, tags=["Cart"])
def get_cart(db: Session=Depends(get_db), current_user: schemas.TokenData=Depends(user_only)):
    try:
        validate_user(current_user.user_id, db)
    except Exception as e:
        raise e

    cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.user_id).all()
    
    return cart

@router.post("/me/cart", response_model=schemas.CartOut, status_code=status.HTTP_201_CREATED, tags=["Cart"])
def add_to_cart(request: schemas.CartItem, db: Session=Depends(get_db), current_user: schemas.TokenData=Depends(user_only)):
    try:
        validate_book(request.book_id, db)
        validate_user(current_user.user_id, db)
    except Exception as e:
        raise e

    cart_item = db.query(models.Cart).filter(models.Cart.user_id == current_user.user_id,
                                             models.Cart.book_id == request.book_id).first()
    if cart_item:
        cart_item.quantity += request.quantity
        db.commit()
        db.refresh(cart_item)
        return cart_item
    
    new_cart_item = models.Cart(
        user_id = current_user.user_id,
        book_id = request.book_id,
        quantity = request.quantity
    )

    db.add(new_cart_item)
    db.commit()
    db.refresh(new_cart_item)

    return new_cart_item

@router.delete("/me/cart", status_code=status.HTTP_200_OK, tags=["Cart"])
def remove_from_cart(request: schemas.CartItem, db: Session=Depends(get_db), current_user: schemas.TokenData=Depends(user_only)):
    try:
        validate_book(request.book_id, db)
        validate_user(current_user.user_id, db)
    except Exception as e:
        raise e
    
    cart_item = db.query(models.Cart).filter(models.Cart.user_id == current_user.user_id,
                                             models.Cart.book_id == request.book_id).first()
    
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book does not exist in cart")
    
    if cart_item.quantity - request.quantity > 0:
        cart_item.quantity -= request.quantity
        db.commit()
        db.refresh(cart_item)
        return cart_item
    else:
        db.delete(cart_item)
        db.commit()
        return {"message": "Removed item from cart successfully"}
    
@router.delete("/me/cart/clear", status_code=status.HTTP_200_OK, tags=["Cart"])
def clear_cart(db: Session=Depends(get_db), current_user: schemas.TokenData=Depends(user_only)):
    try:
        validate_user(current_user.user_id, db)
    except Exception as e:
        raise e
    
    cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.user_id).all()

    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart is empty")

    db.query(models.Cart).filter(models.Cart.user_id == current_user.user_id).delete(synchronize_session=False)
    db.commit()

    return {"message": "Cart Cleared"}
    
@router.get("/me/purchases", response_model= List[schemas.PurchaseOut], status_code=status.HTTP_200_OK, tags=["Purchase"])
def get_all_purchases(db: Session=Depends(get_db), current_user: schemas.TokenData=Depends(user_only)):
    try:
        validate_user(current_user.user_id, db)
    except Exception as e:
        raise e
        
    purchases = db.query(models.Purchase).filter(models.Purchase.user_id == current_user.user_id).all()
        
    return purchases
    
@router.post("/me/purchases", status_code=status.HTTP_201_CREATED, tags=["Purchase"])
def purchase_book(request: schemas.PurchaseCreate, db: Session=Depends(get_db), current_user: schemas.TokenData=Depends(user_only)):
    try:
        validate_book(request.book_id, db)
        validate_user(current_user.user_id, db)
    except Exception as e:
        raise e

    new_purchase=models.Purchase(
        user_id = current_user.user_id,
        book_id = request.book_id,
        quantity = request.quantity
    )

    db.add(new_purchase)
    db.commit()
    db.refresh(new_purchase)

    return {"message": "Purchase successful",
            "Purchase id": new_purchase.id}

@router.post("/me/checkout", status_code=status.HTTP_201_CREATED, tags=["Purchase", "Cart"])
def checkout_cart(db: Session=Depends(get_db), current_user: schemas.TokenData=Depends(user_only)):
    try:
        validate_user(current_user.user_id, db)
    except Exception as e:
        raise e
    
    cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.user_id).all()

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

    db.query(models.Cart).filter(models.Cart.user_id == current_user.user_id).delete(synchronize_session=False)
    db.commit()

    return {"message": "Purchase Successful"}

@router.delete("/me/purchases/{book_id}", status_code=status.HTTP_201_CREATED, tags=["Purchase"])
def refund_book(book_id: int, db: Session=Depends(get_db), current_user: schemas.TokenData=Depends(user_only)):
    try:
        validate_book(book_id, db)
        validate_user(current_user.user_id, db)
    except Exception as e:
        raise e
    
    purchase = db.query(models.Purchase).filter(models.Purchase.user_id == current_user.user_id,
                                                models.Purchase.book_id == book_id).first()
    
    if purchase:
        db.delete(purchase)
        db.commit()
        return {"message": "Refund successful"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Purchase doesn't exist"})