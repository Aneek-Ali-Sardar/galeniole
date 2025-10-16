from motor.motor_asyncio import AsyncIOMotorClient

# replace <db_password> with your real password (no < > symbols)
MONGO_URL = "mongodb+srv://admin:MGD5UbCq@cluster0.eptl4zn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# create a connection
client = AsyncIOMotorClient(MONGO_URL)
db = client.healthcare  # 'healthcare' will be your database name

# test connection
async def test_connection():
    try:
        await db.command("ping")
        print("✅ MongoDB connected successfully!")
    except Exception as e:
        print("❌ Connection error:", e)