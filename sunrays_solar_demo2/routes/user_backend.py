import uuid
from argon2.exceptions import VerifyMismatchError
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from argon2 import PasswordHasher
from schemas.user_schema import CreateUser, UpdateUser
from models import database_models

hash_password = PasswordHasher()


async def get_create_admin(db: AsyncSession, user: CreateUser):
    user.password = hash_password.hash(user.password)

    db_user = database_models.User(**user.dict(exclude_none=True), active=True, token=uuid.uuid4().hex)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_create_user(db: AsyncSession, user_id, user: CreateUser):
    user.password = hash_password.hash(user.password)

    db_user = database_models.User(**user.dict(exclude_none=True), created_by=user_id)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_db_user_email(db: AsyncSession, email):
    stmt = select(database_models.User).where(database_models.User.email == email)
    result = await db.execute(stmt)
    return result.scalar()


async def get_db_user_token(db: AsyncSession, token):
    stmt = select(database_models.User).where(database_models.User.token == token)
    result = await db.execute(stmt)
    return result.scalar()


async def get_all_db_user(db: AsyncSession):
    stmt = select(database_models.User)
    result = await db.execute(stmt)
    return result.scalars().all()


async def user_get_all_db_user(db: AsyncSession):
    stmt = select(database_models.User).where(database_models.User.user_type == 1)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_update_user(db, token, user_schema: UpdateUser):
    db_user = await get_db_user_token(db, token)
    for field, value in user_schema.dict(exclude_unset=True).items():
        setattr(db_user, field, value)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_db_user_by_id(db: AsyncSession, table, column1, value1):
    stmt = select(table).where(column1 == value1)
    result = await db.execute(stmt)
    return result.scalar()


async def check_password(hashed_password: str, password: str):
    try:
        return hash_password.verify(hashed_password, password)
    except VerifyMismatchError:
        return False


async def update_user_token(db: AsyncSession, user: database_models.User):
    stmt = update(database_models.User).where(database_models.User.id == user.id).values(token=uuid.uuid4().hex,
                                                                                         active=True)
    await db.execute(stmt)
    await db.commit()
    await db.refresh(user)
    return user


async def update_fcm_token(db: AsyncSession, user: database_models.User, fcm_token: str):
    stmt = update(database_models.User).where(database_models.User.id == user.id).values(fcm_token=fcm_token)

    await db.execute(stmt)
    await db.commit()
    await db.refresh(user)
    return user

