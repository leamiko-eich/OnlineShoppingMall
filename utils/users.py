import uuid
from typing import Optional
from typing import AsyncGenerator
from fastapi import Depends, Request
from sqlalchemy.orm import DeclarativeBase
from fastapi_users import schemas, BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from fastapi_users.authentication import (AuthenticationBackend, BearerTransport, JWTStrategy,)


SECRET = "SECRET"
DATABASE_URL = "sqlite+aiosqlite:///utils/database.db"
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass


async def create_db_and_tables():
    """
    使用提供的引擎创建数据库及其表的函数。
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    使用async_session_maker异步生成异步会话。
    产生一个AsyncSession对象。
    """
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    返回SQLAlchemyUserDatabase实例的协同程序
    通过在给定AsyncSession作为输入的情况下生成它。
    """
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        """
        在用户注册后调用的一种方法。

        参数：
            user（user）：已注册的用户。
            request（request，可选）：与注册相关联的请求。默认为“无”。
        """
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        """
        用于处理用户忘记密码后的操作。

        参数：
            user（user）：忘记密码的用户。
            token（str）：密码的重置令牌。
            request（可选[请求]）：正在提出的请求（如果可用）。
        """
        reset_API = "http://localhost:8000/auth/jwt/change-password"
        print(f"User {user.id} has forgot their password. Reset token: {token}")
        print(f"URL: {reset_API}/{token}")

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        """
        对整个函数、在请求后验证。
        """
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    """
    使用提供的SQLAlchemyUserDatabase生成UserManager实例的协同程序。
    接受SQLAlchemyUserDatabase对象作为可选参数。
    """
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    """
    返回一个JWTStrategy对象，该对象具有特定的机密和生存期（以秒为单位）。
    """
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)


"""
schemas模块包含了一些用户模型的基本结构，如UserRead，UserCreate，UserUpdate。
"""


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


