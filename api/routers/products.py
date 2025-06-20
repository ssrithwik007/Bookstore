from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
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

@router.post("/", status_code=status.HTTP_201_CREATED)
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

@router.delete("/{book_id}", status_code=status.HTTP_200_OK)
def delete_book(book_id: int, db: Session=Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).delete(synchronize_session=False)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    db.commit()
    return {"message": "Book deleted successfully"}

@router.put("/{book_id}", status_code=status.HTTP_200_OK)
def update_book(book_id: int, request: schemas.BookCreate, db: Session=Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id)
    if book.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    book.update(request.model_dump())
    
    db.commit()
    return {"Product successfully updated."}