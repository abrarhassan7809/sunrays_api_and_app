from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from models import database_models
from routes.authentication import authenticate_user, authenticate_admin
from routes.user_backend import get_create_user, get_all_db_user, get_update_user, get_db_user_email, \
    check_password, update_user_token, update_fcm_token, get_db_user_token, get_db_user_by_id, user_get_all_db_user
from schemas.user_schema import CreateUser, GetUser, UpdateUser, UserLogin, FcmToken
from models.database_config import get_db

router = APIRouter()


# ======users=======
@router.post('/login/', response_model=GetUser, status_code=status.HTTP_200_OK)
async def user_login(user_schema: UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = await get_db_user_email(db, user_schema.email)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Credential",
        )
    if not await check_password(db_user.password, user_schema.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Credential",
        )
    update_token = await update_user_token(db, db_user)

    return update_token


@router.post("/logout/", status_code=status.HTTP_200_OK)
async def logout(response: Response, db: AsyncSession = Depends(get_db),
                 current_user=Depends(authenticate_user)):
    if current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    response.delete_cookie(key="token")
    current_user.token = None
    await db.commit()
    return {"message": "Logged out successfully"}


# @router.post("/upsert_fcm_token/", status_code=status.HTTP_200_OK)
# async def upsert_fcm_token(user: FcmToken, db: AsyncSession = Depends(get_db)):
#     update_token = await update_fcm_token(db, current_user, user.fcm_token)
#     return update_token


@router.post('/create_user/', response_model=GetUser, status_code=status.HTTP_201_CREATED)
async def create_user(user_schema: CreateUser, db: AsyncSession = Depends(get_db),
                      current_user=Depends(authenticate_admin)):
    if current_user.user_type == 0:
        if await get_db_user_email(db, user_schema.email) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with same email exists",
            )

        db_user = await get_create_user(db, current_user.id, user_schema)
        return db_user

    return {'detail': 'must be admin'}


@router.get('/get_user/', response_model=GetUser, status_code=status.HTTP_200_OK)
async def get_user(db: AsyncSession = Depends(get_db), current_user=Depends(authenticate_user)):
    db_user = await get_db_user_token(db, current_user.token)
    return db_user


@router.get('/get_all_user/', status_code=status.HTTP_200_OK)
async def get_all_user(db: AsyncSession = Depends(get_db), current_user=Depends(authenticate_user)):
    if current_user.user_type == 0:
        db_admin = await get_all_db_user(db)
        return db_admin

    db_user = await user_get_all_db_user(db)
    return db_user


@router.delete('/delete_user/{user_id}/', status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(authenticate_user)):
    db_data = await get_db_user_by_id(db, database_models.User, database_models.User.id, user_id)
    if current_user.user_type == 0:
        if db_data is None:
            return {'detail': 'Empty'}
        await db.delete(db_data)
        await db.commit()
        return {'detail': 'user deleted successfully'}

    return {'detail': 'must be admin'}


@router.patch('/update_user/', response_model=GetUser, status_code=status.HTTP_200_OK)
async def update_user(user_schema: UpdateUser, db: AsyncSession = Depends(get_db),
                      current_user=Depends(authenticate_user)):
    if current_user.user_type == 0:
        db_user = await get_update_user(db, current_user.token, user_schema)
        return db_user

    return {'detail': 'must be admin'}
