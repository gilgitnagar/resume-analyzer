# pyrefly: ignore [missing-import]
from sqlalchemy import create_engine, Column, Integer, String
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import declarative_base, sessionmaker
# pyrefly: ignore [missing-import]
from sqlalchemy.exc import IntegrityError

# DATABASE
DATABASE_URL = "sqlite:///users.db"

engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# USER TABLE
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

# CREATE DATABASE
def init_db():
    Base.metadata.create_all(bind=engine)

# CREATE USER
def create_user(username, password):
    session = SessionLocal()
    try:
        user = User(username=username, password=password)
        session.add(user)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False
    finally:
        session.close()

# LOGIN USER
def login_user(username, password):
    session = SessionLocal()
    user = session.query(User).filter_by(username=username, password=password).first()
    session.close()
    return user is not None