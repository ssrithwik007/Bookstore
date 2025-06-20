from fastapi import FastAPI
from . import models
from .database import engine
from .routers import books, users, login
from dotenv import load_dotenv
from .routers.users import init_admin
import os

app = FastAPI(
    title="Rithwik's Bookstore API",
    description='''API for my bookstore website. [GitHub Repo](https://github.com/ssrithwik007/Bookstore)''',
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

    
