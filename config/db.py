import os
from motor.motor_asyncio import AsyncIOMotorClient

# Get MongoDB URL from Render environment variable
MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise ValueError("❌ MONGO_URL environment variable not set!")

# Create a connection
client = AsyncIOMotorClient(MONGO_URL)
db = client.healthcare  # 'healthcare' will be your database name

# Optional: test connection
async def test_connection():
    try:
        await db.command("ping")
        print("✅ MongoDB connected successfully!")
    except Exception as e:
        print("❌ Connection error:", e)