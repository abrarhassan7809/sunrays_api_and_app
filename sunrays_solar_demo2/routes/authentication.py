from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.database_config import get_db
from routes.user_backend import get_db_user_token

bearer_schema = HTTPBearer()


async def authenticate_admin(
        db: AsyncSession = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    db_user = await get_db_user_token(db, token.credentials)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not exist or Invalid authentication credentials",
        )
    if not db_user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not activated",
        )
    if db_user.user_type != 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Must be admin",
        )

    return db_user


async def authenticate_user(db: AsyncSession = Depends(get_db),
                            token: HTTPAuthorizationCredentials = Depends(bearer_schema)):
    db_user = await get_db_user_token(db, token.credentials)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication credentials",
        )
    if not db_user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not activated",
        )

    return db_user


async def get_db_user(db: AsyncSession, table, column1, value1):
    stmt = select(table).where(column1 == value1)
    result = await db.execute(stmt)
    return result.scalar()
