from fastapi import FastAPI
from . import models
from .database import engine
from .routers import products, users

app = FastAPI(
    title="Rithwik's Bookstore API",
    description='''API for my bookstore website. [GitHub Repo](https://github.com/ssrithwik007/Bookstore)''',
)

app.include_router(products.router)
app.include_router(users.router)

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Read docs at /docs"}

    
