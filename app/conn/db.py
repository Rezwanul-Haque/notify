from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, JSON)
from databases import Database

from app.config import get_settings

settings = get_settings()
DATABASE_URL = f'mysql://{settings.db_user}:{settings.db_pass}@{settings.db_host}/{settings.db_schema}'

database = Database(DATABASE_URL)

metadata = MetaData()

user_devices = Table(
    'user_devices',
    metadata,
    Column("id", Integer, primary_key=True),
    Column('user_id', Integer, nullable=False),
    Column('token', String(255), unique=True, nullable=False),
    Column('device_info', JSON, nullable=True)
)

engine = create_engine(DATABASE_URL)



