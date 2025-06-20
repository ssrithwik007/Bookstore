from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from .login import trail_admin_plus
from typing import List

router = APIRouter(
    tags=["Books"],
    prefix="/books"
)

@router.get("/", response_model=List[schemas.BookOut], status_code=status.HTTP_200_OK)
def get_books(db: Session=Depends(get_db)):
    books = db.query(models.Book).all()
    return books

@router.get("/{book_id}", response_model=schemas.BookOut, status_code=status.HTTP_200_OK)
def get_book(book_id: int, db: Session=Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

@router.post("/", response_model=schemas.BookOut, status_code=status.HTTP_201_CREATED)
def add_book(request: schemas.BookCreate, db: Session=Depends(get_db), current_user: schemas.TokenData=Depends(trail_admin_plus)):
    existing_book = db.query(models.Book).filter(models.Book.name == request.name,
                                                 models.Book.author == request.author).first()
    
    if existing_book:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Book already exists in inventory")

    new_book = models.Book(
        name = request.name,
        author = request.author,
        description = request.description,
        genre = request.genre,
        price = request.price,
        added_by_id = current_user.user_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.delete("/{book_id}", status_code=status.HTTP_200_OK)
def delete_book(book_id: int, db: Session=Depends(get_db), current_user: schemas.TokenData=Depends(trail_admin_plus)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    if current_user.role == "trail_admin" and book.added_by_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete books which are not added by you.")

    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}

@router.put("/{book_id}", response_model=schemas.BookOut, status_code=status.HTTP_200_OK)
def update_book(book_id: int, request: schemas.BookUpdate, db: Session=Depends(get_db), current_user: schemas.TokenData=Depends(trail_admin_plus)):
    book = db.query(models.Book).filter(models.Book.id == book_id)
    if book.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    if current_user.role == "trail_admin" and book.first().added_by_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot update books which are not added by you.")
    
    duplicate = db.query(models.Book).filter(
        models.Book.name == request.name,
        models.Book.author == request.author,
        models.Book.id != book_id
    ).first()

    if duplicate:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Another book with same name and author already exists")
    
    book.update(request.model_dump(exclude_unset=True))
    
    db.commit()
    return book.first()