"""
JWT token utilities
"""
import jwt
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from config import Config


def create_access_token(data: Dict[str, Any]) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=Config.JWT_EXPIRATION_DAYS)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.JWT_ALGORITHM)


def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify a JWT access token. Returns payload if valid, None if invalid."""
    try:
        return jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
    except jwt.PyJWTError:
        return None
