"""
MiauAuth - osu! OAuth Identity Provider
Issues JWT tokens with osu! user data for easy integration.
"""
import base64
from typing import Optional
from fastapi import FastAPI, Request, Query
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from config import Config
from utils.osu_api import OsuAPI
from utils.jwt_utils import create_access_token, verify_access_token

app = FastAPI(
    title="MiauAuth",
    description="osu! OAuth Identity Provider",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.get("/")
def read_root():
    return {"name": "MiauAuth", "version": "1.0.0", "status": "running"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/auth/login")
async def login(request: Request):
    """Initiate osu! OAuth flow"""
    origin = request.headers.get("referer", "") or Config.DEFAULT_REDIRECT
    state = base64.urlsafe_b64encode(origin.encode()).decode()
    return RedirectResponse(url=OsuAPI.get_auth_url(state=state), status_code=302)


@app.get("/auth/callback")
async def callback(
    code: str = Query(..., description="Authorization code from osu!"),
    state: Optional[str] = Query(None, description="State parameter for origin tracking"),
):
    """
    Handle OAuth callback from osu!
    Exchange code for token, get user info, create JWT, redirect to frontend
    """
    redirect_origin = Config.DEFAULT_REDIRECT
    if state:
        try:
            redirect_origin = base64.urlsafe_b64decode(state.encode()).decode()
        except Exception:
            pass

    if not code:
        return RedirectResponse(url=f"{redirect_origin}?error=no_code", status_code=302)

    access_token = await OsuAPI.exchange_code_for_token(code)
    if not access_token:
        return RedirectResponse(url=f"{redirect_origin}?error=auth_failed", status_code=302)

    osu_user = await OsuAPI.get_user_info(access_token)
    if not osu_user:
        return RedirectResponse(url=f"{redirect_origin}?error=user_failed", status_code=302)

    # Create JWT with osu! user data
    token = create_access_token({
        "osu_id": osu_user["id"],
        "username": osu_user["username"],
        "country_code": osu_user.get("country_code", "XX"),
        "avatar_url": osu_user.get("avatar_url", ""),
    })

    return RedirectResponse(url=f"{redirect_origin}?token={token}", status_code=302)


@app.get("/auth/verify")
async def verify(token: str = Query(..., description="JWT token to verify")):
    """Verify a JWT token and return the payload if valid."""
    payload = verify_access_token(token)
    if not payload:
        return JSONResponse(status_code=401, content={"valid": False, "error": "Invalid or expired token"})
    return {"valid": True, "user": payload}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=Config.DEBUG
    )
