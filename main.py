from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import users, products, orders, categories, reviews

Base.metadata.create_all(bind=engine)  # Tabloları oluştur

app = FastAPI()

app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(categories.router)
app.include_router(reviews.router)