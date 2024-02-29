import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient
from pymongo.database import Database
from pymongo.collection import Collection
from test.test import test
from src.bot import start
from src.config import conf


async def main():
    client: AgnosticClient = AsyncIOMotorClient(conf.mongodb_url)
    db: Database = client.get_database(conf.db_name.get_secret_value())
    collection: Collection = db.get_collection(conf.coll_name.get_secret_value())
    await test(collection)
    await start(collection)

if __name__ == '__main__':
    asyncio.run(main())
