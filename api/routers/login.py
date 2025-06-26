from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from passlib.context import CryptContext
from dotenv import load_dotenv
from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

@router.post("/login", tags=["Authentication"])
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username doesn't exist/not found")
    
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")
    
    access_token = generate_token(data = {"user_id": user.id,
                                          "role": user.role})

    return {"access_token": access_token,
            "role": user.role,
            "username": user.username,
            "token_type": "Bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                   detail="Invalid authorization credentials",
                                   headers={'WWW-AUTHENTICATE': "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY,  algorithms=[JWT_ALGORITHM])
        user_id: int = payload.get("user_id")
        role: str = payload.get("role")
        if user_id is None or role is None:
            raise cred_exception
        return schemas.TokenData(user_id=user_id, role=role)
    except JWTError:
        raise cred_exception
    
def admin_only(current_user: schemas.TokenData = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user

def user_only(current_user: schemas.TokenData = Depends(get_current_user)):
    if current_user.role != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User access only")
    return current_user

def trail_admin_plus(current_user: schemas.TokenData = Depends(get_current_user)):
    if current_user.role not in ["admin", "trail_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin/Trail Admin access required")
    return current_user

def trail_admin_nd_user(current_user: schemas.TokenData = Depends(get_current_user)):
    if current_user.role not in ["user", "trail_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Trail Admin/User access only")
    return current_user