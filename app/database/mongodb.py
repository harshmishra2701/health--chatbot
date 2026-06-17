from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings


client = AsyncIOMotorClient(settings.MONGODB_URI)

database = client[settings.DATABASE_NAME]


chat_collection = database.chats
