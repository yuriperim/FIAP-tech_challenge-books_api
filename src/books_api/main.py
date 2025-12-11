from fastapi import FastAPI

from .routers import admin


app = FastAPI()
app.include_router(admin.router)


@app.get("/")
async def get_root():
    return {"message": "Tech Challenge - Books API"}
