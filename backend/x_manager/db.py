import os
import motor.motor_asyncio
from beanie import init_beanie
from .models.Followers import Follower
from .models.Following import Following
from .models.Likes import Like
from .models.Tweet import Tweet

MONGODB_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME", "root")
MONGODB_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "example")
MONGODB_PORT = os.getenv("MONGO_INITDB_PORT", "27017")
MONGODB_DATABASE = os.getenv("MONGO_INITDB_DATABASE", "main")
MONGODB_SERVICE_NAME = os.getenv("MONGO_INITDB_SERVICE_NAME", "mongo")

MONGODB_URI = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_SERVICE_NAME}:{MONGODB_PORT}/{MONGODB_DATABASE}"


async def start_db():
    """Starts MongoDB Connection and initializes Models"""
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
    database = client[MONGODB_DATABASE]
    await init_beanie(
        database=database, document_models=[Follower, Following, Like, Tweet]
    )
