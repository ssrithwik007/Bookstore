from fastapi import FastAPI, status, Response, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from . import schemas, models
from .database import engine, SessionLocal, get_db
from typing import List

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Read docs at /docs"}

@app.get("/books", response_model=List[schemas.BookOut], status_code=status.HTTP_200_OK, tags=["Books"])
def get_books(db: Session=Depends(get_db)):
    books = db.query(models.Book).all()
    return books

@app.get("/books/{book_id}", response_model=schemas.BookOut, status_code=status.HTTP_200_OK, tags=["Books"])
def get_book(book_id: int, db: Session=Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

@app.post("/books", status_code=status.HTTP_201_CREATED, tags=["Books"])
def add_book(request: schemas.BookCreate, db: Session=Depends(get_db)):
    new_book = models.Book(
        name = request.name,
        author = request.author,
        description = request.description,
        genre = request.genre,
        price = request.price
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return request

@app.delete("/books/{book_id}", status_code=status.HTTP_200_OK, tags=["Books"])
def delete_book(book_id: int, db: Session=Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).delete(synchronize_session=False)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    db.commit()
    return {"message": "Book deleted successfully"}

@app.put("/books/{book_id}", status_code=status.HTTP_200_OK, tags=["Books"])
def update_book(book_id: int, request: schemas.BookCreate, db: Session=Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id)
    if book.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    book.update(request.model_dump())
    
    db.commit()
    return {"Product successfully updated."}

@app.get("/users/{user_id}", response_model=schemas.UserOut, status_code=status.HTTP_200_OK, tags=["Users"])
def get_user(user_id: int, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@app.get("/users", response_model=List[schemas.UserOut], status_code=status.HTTP_200_OK, tags=["Users"])
def get_all_users(db: Session=Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.post("/users", status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(request: schemas.UserCreate, db: Session=Depends(get_db)):
    new_user = models.User(
        username = request.username,
        email = request.email,
        password = request.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"User created successfully"}

@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["Users"])
def delete_user(user_id: int, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).delete(synchronize_session=False)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.commit()
    return {"User Removed Successfully"}

@app.put("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["Users"])
def update_user(user_id: int, request: schemas.UserCreate, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id)
    if user.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user.update(request.model_dump())

    db.commit()
    return {"User successfully updated"}


def validate_user(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

def validate_book(book_id: int, db: Session):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

@app.get("/users/{user_id}/cart", response_model=List[schemas.CartOut], status_code=status.HTTP_200_OK, tags=["Cart"])
def get_cart(user_id: int, db: Session=Depends(get_db)):
    try:
        validate_user(user_id, db)
    except Exception as e:
        raise e

    cart = db.query(models.Cart).filter(models.Cart.user_id == user_id).all()

    if not cart:
        return {"Cart is Empty"}  
    
    return cart

@app.post("/users/{user_id}/cart", response_model=schemas.CartOut, status_code=status.HTTP_201_CREATED, tags=["Cart"])
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

@app.delete("/users/{user_id}/cart", status_code=status.HTTP_200_OK, tags=["Cart"])
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
    
@app.get("/users/{user_id}/purchases", response_model= List[schemas.PurchaseOut], status_code=status.HTTP_200_OK, tags=["Purchase"])
def get_all_purchases(user_id: int, db: Session=Depends(get_db)):
    try:
        validate_user(user_id, db)
    except Exception as e:
        raise e
        
    purchases = db.query(models.Purchase).filter(models.Purchase.user_id == user_id).all()

    if not purchases:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No purchase history found")
        
    return purchases
    
@app.post("/users/{user_id}/purchases", status_code=status.HTTP_201_CREATED, tags=["Purchase"])
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

@app.post("/users/{user_id}/checkout", status_code=status.HTTP_201_CREATED, tags=["Purchase", "Cart"])
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

@app.delete("/users/{user_id}/purchases/{book_id}", status_code=status.HTTP_201_CREATED, tags=["Purchase"])
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
    
