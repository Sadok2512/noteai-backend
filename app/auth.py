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
    if data.email == "demo@demo.com" and data.password == "demo":
        return {"user_id": "demo-user", "email": data.email}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# 🆕 Fake register (accepte tout sauf test@test.com)
@router.post("/auth/register")
def register_user(data: AuthData):
    if data.email == "test@test.com":
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"user_id": "registered-" + data.email.split("@")[0], "email": data.email}
