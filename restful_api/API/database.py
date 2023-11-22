from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = "sqlite:///sql_app.db"

# iot_project_password

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:iot_project_password@db.lyqfqgsowtubylckeiko.supabase.co:5432/postgres"



engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
