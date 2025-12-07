from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# настрйоки для подключения к нашей бд
DB_HOST = os.getenv("DB_HOST")
DP_PORT = os.getenv("DP_PORT")
DP_USER = os.getenv("DP_USER")
DP_PASS = os.getenv("DP_PASS")
DB_NAME = os.getenv("DB_NAME")

# Если DP_PORT пуст или None, используем значение по умолчанию (5432)

# схема для подключения к sqlalchemy
DATABASE_URL = f"postgresql+asyncpg://{DP_USER}:{DP_PASS}@{DB_HOST}:{DP_PORT}/{DB_NAME}"

# асинхронный движок который знает как подключаться и управляет соединениями
engine = create_async_engine(DATABASE_URL)

# создается фабрика сессий для подключения к бд 
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# для миграций указываем что у нас декларативный стиль
class Base(DeclarativeBase):
    pass
