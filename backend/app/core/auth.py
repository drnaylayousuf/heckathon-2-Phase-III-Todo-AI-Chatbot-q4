from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from sqlmodel import Session
from app.database.session import get_session
from app.models.user import User
from app.schemas.user import TokenData
from app.config import settings
import warnings
import bcrypt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hashed password."""
    try:
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except ValueError:
        return False

def get_password_hash(password: str) -> str:
    """Hash a plaintext password."""
    # Truncate password if it exceeds bcrypt's 72-byte limit
    if len(password.encode('utf-8')) > 72:
        password = password[:72]
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

security = HTTPBearer()

# Secret key for JWT - must be set in production environment
SECRET_KEY = settings.secret_key
if SECRET_KEY == "dev-secret-key-for-development-only-change-in-production":
    warnings.warn(
        "Using default development SECRET_KEY. This is insecure for production. "
        "Please set SECRET_KEY environment variable in production.",
        UserWarning
    )

ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password."""
    user = session.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    credentials: HTTPBearer = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """Get the current user from the JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: str = payload.get("user_id")

        if email is None or user_id is None:
            raise credentials_exception

        token_data = TokenData(user_id=user_id, email=email)
    except JWTError:
        raise credentials_exception

    user = session.query(User).filter(User.id == token_data.user_id).first()

    if user is None:
        raise credentials_exception

    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get the current active user."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def create_user(session: Session, email: str, password: str, name: Optional[str] = None) -> User:
    """Create a new user with hashed password."""
    hashed_password = get_password_hash(password)
    db_user = User(
        email=email,
        password_hash=hashed_password,
        name=name
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user