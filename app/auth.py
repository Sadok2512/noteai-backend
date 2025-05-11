
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta
from pymongo import MongoClient
from jose import jwt
from passlib.context import CryptContext

router = APIRouter()

# Config
SECRET_KEY = "noteai-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# MongoDB
client = MongoClient("mongodb+srv://sadokbenali:<db_password>@noteai.odx94om.mongodb.net/?retryWrites=true&w=majority&appName=NoteAI")
db = client["noteai"]
users_collection = db["users"]

# Password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthData(BaseModel):
    email: EmailStr
    password: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/auth/register")
def register_user(data: AuthData):
    existing_user = users_collection.find_one({"email": data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(data.password)
    user = {"email": data.email, "password": hashed_password}
    users_collection.insert_one(user)

    token = create_access_token({"sub": data.email}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"user_id": str(user["_id"]), "email": data.email, "token": token}
