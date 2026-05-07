# pyrefly: ignore [missing-import]
from passlib.context import CryptContext
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from models import User

# Use pbkdf2_sha256 instead of bcrypt
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def register_user(db: Session, username: str, password: str):

    # Check existing user
    existing_user = db.query(User).filter(
        User.username == username
    ).first()

    if existing_user:
        return False

    # Hash password
    hashed_password = hash_password(password)

    # Create user
    new_user = User(
        username=username,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()

    return True


def login_user(db: Session, username: str, password: str):

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:
        return False

    if verify_password(password, user.password):
        return True

    return False