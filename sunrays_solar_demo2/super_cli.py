import argparse
import asyncio
import json

from models.database_config import SessionLocal
from models import database_models
from routes.authentication import get_db_user
from routes.user_backend import get_create_admin
from schemas.user_schema import CreateUser, GetUser

parser = argparse.ArgumentParser(
    prog="vcsdx",
    description="CRUD operations for super admin",
    argument_default=None,
    add_help=True,
)
subparsers = parser.add_subparsers(help="command help")
parser_a = subparsers.add_parser("createsuperuser", help="create a new super user.")
parser_a.add_argument("--email", type=str, required=True)
parser_a.add_argument("--password", type=str, required=True)
parser_a.add_argument("--first_name", type=str, required=True)
parser_a.add_argument("--last_name", type=str, required=True)


args = parser.parse_args()


async def do_register_super_user(
    input_email: str, f_name: str, l_name: str, input_password: str
):
    async with SessionLocal() as db:
        if await get_db_user(db, database_models.User, database_models.User.email, input_email) is not None:
            raise ValueError("User with same email exists")

        user = CreateUser(
            first_name=f_name,
            last_name=l_name,
            email=input_email,
            password=input_password,
            user_type=0,
        )
        adduser = await get_create_admin(db, user)
        print(GetUser.from_orm(adduser).dict())


if parser_a:
    email = args.email
    password = args.password
    first_name = args.first_name
    last_name = args.last_name
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        do_register_super_user(email, first_name, last_name, password)
    )
