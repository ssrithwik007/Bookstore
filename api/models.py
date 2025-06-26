from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from .database import Base
from .schemas import RoleEnum

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    author = Column(String)
    description = Column(String)
    genre = Column(String)
    price = Column(Float)
    added_by_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))

    added_by = relationship("User", back_populates="books_added")
    cart_items = relationship("Cart", back_populates="book", cascade="all, delete", passive_deletes=True)
    purchases = relationship("Purchase", back_populates="book", cascade="all, delete", passive_deletes=True)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(SQLAlchemyEnum(RoleEnum, name="role_enum"), default=RoleEnum.user, nullable=False)

    books_added = relationship("Book", back_populates="added_by", cascade="all, delete")
    cart_items = relationship("Cart", back_populates='user', cascade="all, delete")
    purchases = relationship("Purchase", back_populates='user', cascade="all, delete")

class Cart(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    book_id = Column(Integer, ForeignKey('books.id', ondelete="CASCADE"))
    quantity = Column(Integer, default=1)

    user = relationship("User", back_populates='cart_items')
    book = relationship("Book", back_populates="cart_items")

class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    book_id = Column(Integer, ForeignKey('books.id', ondelete="CASCADE"))
    quantity = Column(Integer, default=1)

    user = relationship("User", back_populates='purchases')
    book = relationship("Book", back_populates="purchases")

