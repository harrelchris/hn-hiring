import asyncio
import pathlib
import httpx
import json

from hn import settings


def download_thread(thread_id: int) -> dict:
    response = httpx.get(settings.HACKERNEWS_ITEM_URL.format(item_id=thread_id))
    response.raise_for_status()
    return response.json()


async def download_comments(comment_ids: list[int]) -> list[dict]:
    urls = [settings.HACKERNEWS_ITEM_URL.format(item_id=i) for i in comment_ids]
    client = httpx.AsyncClient()
    responses = await asyncio.gather(*[client.get(url) for url in urls])
    await client.aclose()
    return [r.json() for r in responses]


def write_comments(thread_id: int, comments: list[dict]) -> None:
    file_path = settings.DATA_DIR / f"thread_{thread_id}.json"
    with open(file_path, "w") as file:
        json.dump(comments, file)


async def coroutine(thread_id: int):
    thread = download_thread(thread_id)
    kids = thread["kids"]
    comments = await download_comments(kids)
    write_comments(thread_id, comments)
