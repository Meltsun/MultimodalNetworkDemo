from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_password(user_password, stored_password):
    return pwd_context.verify(user_password, stored_password)
