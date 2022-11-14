import pathlib

import aiohttp
import aiofiles
import asyncio
import os
import json
from typing import Dict


async def download(url: str, filename: str, headers: Dict[str, str] = None):
    print(f"Downloading {filename}...")

    async with aiofiles.open(filename, 'wb') as f:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                content_length = int(resp.headers["Content-Length"])
                downloaded = 0
                async for data, _ in resp.content.iter_chunks():
                    downloaded += len(data)
                    await f.write(data)
                    print(f"{downloaded} / {content_length} is downloaded")
        await f.flush()


async def parse_input(filename: str, headers: Dict[str, str] = None, output: str = "."):
    path = pathlib.Path(output)
    async with aiofiles.open(filename, "r") as f:
        for line in await f.readlines():
            parts = line.split(",")
            p = str(path.joinpath(parts[0]))
            await download(parts[1], p, headers)

if __name__ == "__main__":
    csv_file = os.getenv("BATCH_FILE")
    headers_str = os.getenv("REQ_HEADERS", '{}')
    output_dir = os.getenv("OUTPUT_DIR", ".")
    h = json.loads(headers_str)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parse_input(csv_file, h, output_dir))
