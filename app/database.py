from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:   
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi', user='postgres',
#                                 password='password123',cursor_factory=RealDictCursor)

#         cursor = conn.cursor()
#         print('Database connection was sucessful')
#         break
#     except Exception as e:
#         print('Connecting to database failed')
#         print(f'The error was {e}')
#         time.sleep(2)