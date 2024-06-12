import motor.motor_asyncio
import os
from beanie import init_beanie
from .models.Followers import Follower
from .models.Following import Following
from .models.Likes import Like
from .models.Tweet import Tweet

MONGODB_HOST = os.getenv("MONGODB_HOST", "localhost")
MONGODB_PORT = os.getenv("MONGODB_PORT", "27017")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "main")
MONGODB_URI = f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DATABASE}"


async def start_db():
    """Starts MongoDB Connection and initializes Models"""
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
    database = client[MONGODB_DATABASE]
    await init_beanie(
        database=database, document_models=[Follower, Following, Like, Tweet]
    )
