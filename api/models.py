from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    author = Column(String)
    description = Column(String)
    genre = Column(String)
    price = Column(Float)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")

    cart_items = relationship("Cart", back_populates='user', cascade="all, delete")
    purchases = relationship("Purchase", back_populates='user', cascade="all, delete")

class Cart(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    book_id = Column(Integer, ForeignKey('books.id'))
    quantity = Column(Integer, default=1)

    user = relationship("User", back_populates='cart_items')
    book = relationship("Book")

class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    book_id = Column(Integer, ForeignKey('books.id'))
    quantity = Column(Integer, default=1)

    user = relationship("User", back_populates='purchases')
    book = relationship("Book")

