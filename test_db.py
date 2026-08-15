import asyncio

from app.database import engine


async def test_connection():
    try:
        async with engine.connect():
            print("DATABASE CONNECTION OK")
    except Exception as e:
        print("DATABASE CONNECTION FAILED")
        print(type(e).__name__)
        print(e)


asyncio.run(test_connection())