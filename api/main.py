from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import books, users, login
from dotenv import load_dotenv
from .routers.users import init_admin
import os

origins = ["http://localhost:5500"]

app = FastAPI(
    title="Rithwik's Bookstore API",
    description='''API for my bookstore website. [GitHub Repo](https://github.com/ssrithwik007/Bookstore)''',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

app.include_router(books.router)
app.include_router(users.router)
app.include_router(login.router)

models.Base.metadata.create_all(bind=engine)

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_UNAME")
ADMIN_PASS = os.getenv("ADMIN_PASS")
init_admin(username=ADMIN_USERNAME, password=ADMIN_PASS)

@app.get("/")
def home():
    return {"message": "Read docs at /docs"}

    
