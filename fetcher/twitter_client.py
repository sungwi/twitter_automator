import logging
from datetime import date, timezone

import tweepy

from .models import TweetData

logger = logging.getLogger(__name__)

TWEET_FIELDS = ["created_at", "entities", "author_id"]
USER_FIELDS = ["username", "name"]
EXPANSIONS = ["author_id"]
MAX_RESULTS_PER_PAGE = 100


class TwitterFetcher:
    """Fetches liked tweets from Twitter API v2 using OAuth 1.0a User Context."""

    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
        access_token_secret: str,
    ):
        self.client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            wait_on_rate_limit=True,
        )
        self.user_id = self._get_authenticated_user_id()

    def _get_authenticated_user_id(self) -> str:
        try:
            resp = self.client.get_me(user_auth=True)
        except tweepy.Unauthorized as e:
            raise RuntimeError(
                "Twitter auth failed — check your OAuth 1.0a credentials"
            ) from e

        if resp.data is None:
            raise RuntimeError(
                "Failed to retrieve authenticated user — check your OAuth credentials"
            )

        logger.info("Authenticated as @%s (id=%s)", resp.data.username, resp.data.id)
        return str(resp.data.id)

    def fetch_liked_tweets(self, since: date | None = None) -> list[TweetData]:
        tweets: list[TweetData] = []

        try:
            paginator = tweepy.Paginator(
                self.client.get_liked_tweets,
                id=self.user_id,
                tweet_fields=TWEET_FIELDS,
                user_fields=USER_FIELDS,
                expansions=EXPANSIONS,
                max_results=MAX_RESULTS_PER_PAGE,
                user_auth=True,
            )

            for response in paginator:
                if not response.data:
                    break

                users = {
                    u.id: u for u in (response.includes.get("users") or [])
                }

                stop_paging = False
                for tweet in response.data:
                    created_at = tweet.created_at
                    if created_at and created_at.tzinfo is None:
                        created_at = created_at.replace(tzinfo=timezone.utc)

                    if since and created_at and created_at.date() < since:
                        stop_paging = True
                        continue

                    author = users.get(tweet.author_id)
                    username = author.username if author else "unknown"
                    name = author.name if author else "Unknown"

                    tweets.append(
                        TweetData(
                            tweet_id=str(tweet.id),
                            text=tweet.text,
                            author_username=username,
                            author_name=name,
                            created_at=created_at,
                            tweet_url=f"https://x.com/{username}/status/{tweet.id}",
                            referenced_urls=_extract_urls(tweet),
                        )
                    )

                if stop_paging:
                    break

        except tweepy.Unauthorized as e:
            raise RuntimeError(f"Twitter auth error: {e}") from e
        except tweepy.TooManyRequests as e:
            logger.warning("Rate limited by Twitter API: %s", e)
            raise
        except tweepy.TwitterServerError as e:
            logger.error("Twitter server error: %s", e)
            raise RuntimeError(f"Twitter server error: {e}") from e
        except tweepy.TweepyException as e:
            logger.error("Twitter API error: %s", e)
            raise RuntimeError(f"Twitter API error: {e}") from e

        logger.info("Fetched %d liked tweets", len(tweets))
        return tweets


def _extract_urls(tweet) -> list[str]:
    if not tweet.entities or "urls" not in tweet.entities:
        return []

    urls: list[str] = []
    for entry in tweet.entities["urls"]:
        expanded = entry.get("expanded_url", entry.get("url", ""))
        if not expanded:
            continue
        # Skip tweet self-reference URLs
        if ("twitter.com/" in expanded or "x.com/" in expanded) and "/status/" in expanded:
            continue
        urls.append(expanded)
    return urls
