from sqlalchemy import Column, TIMESTAMP, func, String, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.infrastructure.db_manager.sql_alchemy.base import BaseModel


class AccountModel(BaseModel):
    __tablename__ = 'accounts'
    account_id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="accounts")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id", ondelete="CASCADE"))
    platform_type = Column(String, nullable=False)
    username = Column(String, nullable=False)
    authentication = Column(JSONB, nullable=False)
    creation_datetime = Column(TIMESTAMP, server_default=func.now())
    update_datetime = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
