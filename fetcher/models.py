from datetime import datetime

from pydantic import BaseModel


class TweetData(BaseModel):
    tweet_id: str
    text: str
    author_username: str
    author_name: str
    created_at: datetime
    tweet_url: str
    referenced_urls: list[str] = []
