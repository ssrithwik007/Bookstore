from fastapi import FastAPI
from . import models
from .database import engine
from .routers import books, users, login

app = FastAPI(
    title="Rithwik's Bookstore API",
    description='''API for my bookstore website. [GitHub Repo](https://github.com/ssrithwik007/Bookstore)''',
)

app.include_router(books.router)
app.include_router(users.router)
app.include_router(login.router)

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Read docs at /docs"}

    
