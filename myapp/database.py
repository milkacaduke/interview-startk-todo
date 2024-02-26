from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from myapp.models.todo import Todo

from myapp.config.config import get_config

async def init_db():
    # client = AsyncIOMotorClient("mongodb://localhost:27017")

    # await init_beanie(
    #     database = client["todo_db"],
    #     document_models = [Todo]
    # )

    mongodb_url = get_config().mongodb_url
    db_name = get_config().db_name

    client = AsyncIOMotorClient(mongodb_url)

    await init_beanie(
        database = client[db_name],
        document_models = [Todo]
    )

