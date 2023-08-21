from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession


# =====functions======
async def get_create_category(db: AsyncSession, table, category_schema, user_id,):
    db_category = table(**category_schema.dict(exclude_none=True), user_id=user_id)

    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def get_db_category(db: AsyncSession, table, column1, column2, value1, value2):
    stmt = select(table).where(and_(column1 == value1, column2 == value2))
    result = await db.execute(stmt)
    return result.scalar()


async def get_db_category_by_id(db: AsyncSession, table, column1, value1):
    stmt = select(table).where(column1 == value1)
    result = await db.execute(stmt)
    return result.scalar()


async def get_all_db_category(db: AsyncSession, table):
    stmt = select(table)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_update_category(db: AsyncSession, table, column1, value1, category_schema):
    db_category = await get_db_category_by_id(db, table, column1, value1)
    if db_category is None:
        return {'detail': 'Empty'}

    for field, value in category_schema.dict(exclude_unset=True).items():
        setattr(db_category, field, value)

    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category
