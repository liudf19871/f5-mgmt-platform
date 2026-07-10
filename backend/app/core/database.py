from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

Base = declarative_base()

async_db_url = settings.DATABASE_URL.replace("mysql+pymysql", "mysql+aiomysql")
engine = create_async_engine(async_db_url, echo=True)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

sync_engine = create_engine(settings.DATABASE_URL, echo=True)

async def get_db():
    async with async_session_maker() as session:
        yield session