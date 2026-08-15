import asyncio
import os

import asyncpg
from dotenv import load_dotenv
from urllib.parse import urlparse, unquote


load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL is missing")

url = urlparse(database_url)

username = unquote(url.username)
password = unquote(url.password)
host = url.hostname
port = url.port or 5432
database = url.path.lstrip("/")


async def test_connection():
    print("HOST:", host, flush=True)
    print("PORT:", port, flush=True)
    print("DATABASE:", database, flush=True)
    print("USER:", username, flush=True)
    print("Connecting...", flush=True)

    try:
        conn = await asyncio.wait_for(
            asyncpg.connect(
                user=username,
                password=password,
                host=host,
                port=port,
                database=database,
            ),
            timeout=10,
        )

        print("ASYNCPG CONNECTION OK", flush=True)

        await conn.close()

    except asyncio.TimeoutError:
        print("CONNECTION TIMEOUT", flush=True)

    except Exception as e:
        print("ASYNCPG CONNECTION FAILED", flush=True)
        print(type(e).__name__, flush=True)
        print(e, flush=True)


asyncio.run(test_connection())