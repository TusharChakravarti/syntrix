from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
from app.core.config import settings


#Create the database engine

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug
)

# create session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)



