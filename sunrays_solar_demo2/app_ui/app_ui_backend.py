from fastapi import Depends
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from models import database_models
from models.database_config import get_db


async def get_db_user(token, db: AsyncSession = Depends(get_db)):
    db_data = select(database_models.User).where(database_models.User.token == token)
    db_result = await db.execute(db_data)

    return db_result.scalar()
