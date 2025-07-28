from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

# this is for Setting up the DB and engine.

# We are using SQLite for simplicity.

DATABASE_URL = "sqlite:///./fitness.db"  # Or use PostgreSQL URI for production

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})




@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
