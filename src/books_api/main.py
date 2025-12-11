from fastapi import FastAPI

from src.books_api.routers import admin
from src.books_api.routers import books


app = FastAPI()
app.include_router(admin.router)
app.include_router(books.router)


@app.get("/")
async def get_root():
    return {"message": "Tech Challenge - Books API"}
