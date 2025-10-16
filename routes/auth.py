from fastapi import APIRouter, HTTPException
from config.db import db
from models.user import User, Userlogin
from passlib.hash import bcrypt

auth_router = APIRouter()

@auth_router.post("/signup")
async def signup(user: User):
    # Check if user already exists
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_pw = bcrypt.hash(user.password)

    # Save user to MongoDB
    await db.users.insert_one({
        "name": user.name,
        "email": user.email,
        "password": hashed_pw
    })

    return {"message": "User created successfully"}


@auth_router.post("/login")
async def login(user: Userlogin):
    # Find user in DB
    existing = await db.users.find_one({"email": user.email})
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify password
    if not bcrypt.verify(user.password, existing["password"]):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    return {"message": f"Welcome {existing['name']}"}