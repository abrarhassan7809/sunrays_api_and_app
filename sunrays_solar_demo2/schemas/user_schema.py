from pydantic import BaseModel, Field, validator, validate_email


class BaseMod(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        schema_extra: dict = {}


class CreateUser(BaseMod):
    first_name: str
    last_name: str
    email: str
    password: str
    created_by: int | None = None
    user_type: int

    @validator("email")
    def validate_email(cls, value):
        if not validate_email(value):
            raise ValueError("Email is invalid")
        return value.lower()

    @validator("password")
    def check_password_length(cls, value):
        if len(value) <= 4:
            raise ValueError("Password must be of 5 character")
        return value


class GetUser(CreateUser):
    id: int
    token: str | None = None
    active: str
    password: str = Field(exclude=True)


class UpdateUser(BaseMod):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    created_by: int | None = None


class UserLogin(BaseMod):
    email: str
    password: str


class FcmToken(BaseMod):
    fcm_token: str
