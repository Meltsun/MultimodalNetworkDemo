from fastapi import HTTPException, Depends, status, APIRouter
from passlib.context import CryptContext
from tortoise.exceptions import IntegrityError
from database.models import User
from view.api.auth import verify_password
from tortoise.exceptions import DoesNotExist
from pydantic import BaseModel
import random
import string

# 创建密码哈希上下文对象
api_register = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 定义一个全局字典来保存用户和对应的验证码
user_verification_codes = {}


def generate_verification_code():
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return code


class UserLogin(BaseModel):
    username: str
    password: str


@api_register.post("/register")
async def register(user_register: UserLogin):
    # 对密码进行哈希处理
    hashed_password = pwd_context.hash(user_register.password)
    try:
        # 将用户名和哈希处理后的密码保存到数据库中
        user = await User.create(username=user_register.username, password_hash=user_register.password)
    except IntegrityError:
        # 如果用户名已经存在，则返回 409 Conflict 错误
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )
    return user


@api_register.post("/login")
async def login(user_data: UserLogin):
    try:
        user = await User.get(username=user_data.username)
        print(user)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    if not await verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    return {"result": 0}
