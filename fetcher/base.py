from datetime import date
from typing import Protocol

from .models import TweetData


class TweetFetcher(Protocol):
    def fetch_liked_tweets(self, since: date) -> list[TweetData]: ...
