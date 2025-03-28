from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.account_management.application.user.extension.user_model import ToUserModel, ToUser
from src.services.account_management.repositories.user import IUserRepository
from src.services.account_management.models.user import User as _UserModel
from src.services.account_management.domain.user import UserEntity


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.__session = session
        self.__identity_map = dict()

    async def create(self, user: UserEntity):
        instance = user @ ToUserModel()
        self.__session.add(instance)
        await self.__session.commit()
        await self.__session.refresh(instance)
        update_user = instance @ ToUser()
        self.__identity_map[instance.public_id] = instance
        return update_user

    async def get(self, user) -> UserEntity:
        pass

    async def get_by_user_public_id(self, public_id: str) -> UserEntity:
        pass

    async def get_by_phone(self, phone: str) -> UserEntity:
        stmt = select(_UserModel).where(_UserModel.primary_phone == phone)
        result = await self.__session.execute(stmt)
        instance: _UserModel = result.scalar_one()
        return instance @ ToUser()

    async def get_by_email(self, email: str) -> UserEntity:
        stmt = select(_UserModel).where(_UserModel.primary_email == email)
        result = await self.__session.execute(stmt)
        instance: _UserModel = result.scalar_one()
        return instance @ ToUser()

    async def get_by_identification(self, identification: str) -> UserEntity:
        stmt = select(_UserModel).where(_UserModel.identifier == identification)
        result = await self.__session.execute(stmt)
        instance: _UserModel = result.scalar_one()
        return instance @ ToUser()

    async def update(self, user):
        instance = user @ ToUserModel
        self.__session.add(instance)
        await self.__session.commit()
        await self.__session.refresh(instance)
        update_user = instance @ ToUser()
        self.__identity_map[instance.user_id] = instance
        return update_user

    async def is_exist(self, user):
        raise NotImplementedError

    @classmethod
    def user_repo(cls, session: AsyncSession):
        return UserRepository(session)