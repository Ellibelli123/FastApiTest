from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://postgres:5324@localhost:5432/le_fitness_test"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Drop and recreate all tables"""
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS bookings CASCADE"))
        conn.commit()

    Base.metadata.create_all(bind=engine)
