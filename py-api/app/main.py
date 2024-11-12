from fastapi import FastAPI
from app.routers import users, products, categories

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])