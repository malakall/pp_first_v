from fastapi import FastAPI
from app.users.router import router as users_router  # Импортируем роутер для пользователей
from app.ml.router import router as ml_router

app = FastAPI()

# Подключаем роутеры
app.include_router(users_router)
app.include_router(ml_router)