import pathlib


ROOT_DIR: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent
DATA_DIR: pathlib.Path = ROOT_DIR / "data"
HACKERNEWS_ITEM_URL: str = "https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
