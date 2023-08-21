from typing import Optional
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pathlib import Path
import os

BASEDIR = os.path.abspath(os.path.join("../", os.pardir))
dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)


POSTGRES_USER: Optional[str] = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD: Optional[str] = os.getenv("POSTGRES_PASSWORD")
POSTGRES_SERVER: Optional[str] = os.getenv("POSTGRES_SERVER", "localhost")
POSTGRES_PORT: Optional[str] = os.getenv("POSTGRES_PORT")
POSTGRES_DB: Optional[str] = os.getenv("POSTGRES_DB", "sunrays")

# DATABASE_URL: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
DATABASE_URL: str = f"postgresql+asyncpg://sunrays:sunrays123@localhost:6000/sunrays"
DEBUG: Optional[bool] = os.getenv("DEBUG", "False") == "True"

engine = create_async_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(expire_on_commit=False, autoflush=False, bind=engine, class_=AsyncSession)

connection = SessionLocal()


class Base(DeclarativeBase):
    pass


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
