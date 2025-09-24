from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession


class Model(DeclarativeBase):
	id: Mapped[int] = mapped_column(primary_key=True)


class DBSettings(BaseSettings):
	DB_NAME: str
	DB_USER: str
	DB_PASSWORD: str
	DB_HOST: str
	DB_PORT: int

	@property
	def DATABASE_URL(self):
		return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

	model_config = SettingsConfigDict(env_file='.env', extra='allow')


db_settings = DBSettings()

engine = create_async_engine(db_settings.DATABASE_URL)

Session = async_sessionmaker(engine)

AsyncSessionMaker = async_sessionmaker[AsyncSession]
