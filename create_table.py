import asyncio
from sqlalchemy import Integer, String, Column, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import config

engine = create_async_engine(config.PG_DSN_ALC, echo=True)
Base = declarative_base()


class User(Base):

    __tablename__ = 'persons_starwars'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), index=True)
    height = Column(String(128), )
    mass = Column(String(128), )
    hair_color = Column(String(128), )
    skin_color = Column(String(128), )
    eye_color = Column(String(128), )
    birth_year = Column(String(128), )
    gender = Column(String(128), )
    homeworld = Column(String(128), )
    films = Column(String, )
    species = Column(String(128), )
    vehicles = Column(String, )
    starships = Column(String, )
    created = Column(String(128), )
    edited = Column(String(128), )
    url = Column(String(128), )



async def get_async_session(
    drop: bool = False, create: bool = False
):

    async with engine.begin() as conn:
        if drop:
            await conn.run_sync(Base.metadata.drop_all)
        if create:
            print(1)
            await conn.run_sync(Base.metadata.create_all)
    async_session_maker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    return async_session_maker


async def main():
    await get_async_session(True, True)

if __name__ == '__main__':
    asyncio.run(main())
