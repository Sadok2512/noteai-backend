
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

router = APIRouter()

# 🔐 Modèle de données pour login/register
class AuthData(BaseModel):
    email: EmailStr
    password: str

# ✅ Démo login : demo@demo.com / demo
@router.post("/auth/login")
def login_user(data: AuthData):
    print(f"🔐 Tentative de login pour {data.email}")
    if data.email == "demo@demo.com" and data.password == "demo":
        return {"user_id": "demo-user", "email": data.email}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# 🆕 Fake register (accepte tout sauf test@test.com)
@router.post("/auth/register")
def register_user(data: AuthData):
    if data.email == "test@test.com":
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"user_id": "registered-" + data.email.split("@")[0], "email": data.email}

from google.oauth2 import id_token
from google.auth.transport import requests as grequests

GOOGLE_CLIENT_ID = "458012046264-krfaorod6gokr817betrmbegea7sliuo.apps.googleusercontent.com"

class GoogleToken(BaseModel):
    token: str

@router.post("/auth/google")
async def google_auth(payload: GoogleToken):
    try:
        idinfo = id_token.verify_oauth2_token(payload.token, grequests.Request(), GOOGLE_CLIENT_ID)
        user_id = idinfo.get("sub")
        email = idinfo.get("email")
        name = idinfo.get("name")
        print(f"🔐 Google login réussi pour {email}")
        return {"user_id": user_id, "email": email, "name": name}
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google token")
