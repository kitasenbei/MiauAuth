import os
import dotenv

dotenv.load_dotenv()

class Config:
    # osu! OAuth
    OSU_CLIENT_ID = os.getenv("OSU_CLIENT_ID", "")
    OSU_CLIENT_SECRET = os.getenv("OSU_CLIENT_SECRET", "")
    OSU_REDIRECT_URI = os.getenv("OSU_REDIRECT_URI", "http://localhost:8001/auth/callback")

    # JWT
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_DAYS = int(os.getenv("JWT_EXPIRATION_DAYS", "7"))

    # CORS - comma-separated list of allowed origins
    ALLOWED_ORIGINS = [
        origin.strip()
        for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
    ]

    # Default redirect after auth (if no referer)
    DEFAULT_REDIRECT = os.getenv("DEFAULT_REDIRECT", "http://localhost:5173")

    # Debug
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
