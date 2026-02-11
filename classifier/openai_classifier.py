import json
import logging
import time

from openai import OpenAI

from fetcher.models import TweetData

from .models import BatchClassificationResult, ClassificationResult, Category
from .prompts import SYSTEM_PROMPT, BATCH_USER_PROMPT_TEMPLATE, SINGLE_USER_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
BASE_DELAY = 1.0  # seconds


class OpenAIClassifier:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini", batch_size: int = 10):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.batch_size = batch_size

    def classify_tweets(self, tweets: list[TweetData]) -> dict[str, ClassificationResult]:
        """Classify tweets in batches. Returns dict mapping tweet_id -> ClassificationResult."""
        results: dict[str, ClassificationResult] = {}

        for i in range(0, len(tweets), self.batch_size):
            batch = tweets[i : i + self.batch_size]
            batch_results = self._classify_batch_with_fallback(batch)
            results.update(batch_results)

        # Ensure every tweet has a classification — default unclassified to "Others"
        for tweet in tweets:
            if tweet.tweet_id not in results:
                logger.warning("Tweet %s was not classified, defaulting to Others", tweet.tweet_id)
                results[tweet.tweet_id] = ClassificationResult(
                    tweet_id=tweet.tweet_id,
                    category="Others",
                    title=tweet.text[:60],
                    tags=["unclassified"],
                )

        return results

    def _classify_batch_with_fallback(self, tweets: list[TweetData]) -> dict[str, ClassificationResult]:
        """Try batch classification; on failure, fall back to individual classification."""
        try:
            return self._classify_batch(tweets)
        except Exception:
            logger.warning(
                "Batch classification failed for %d tweets, falling back to individual", len(tweets)
            )
            results: dict[str, ClassificationResult] = {}
            for tweet in tweets:
                try:
                    single = self._classify_single(tweet)
                    results[single.tweet_id] = single
                except Exception:
                    logger.warning("Individual classification failed for tweet %s", tweet.tweet_id)
            return results

    def _classify_batch(self, tweets: list[TweetData]) -> dict[str, ClassificationResult]:
        """Classify a batch of tweets with retry + exponential backoff."""
        tweets_json = json.dumps(
            [{"tweet_id": t.tweet_id, "text": t.text, "author": t.author_username} for t in tweets],
            indent=2,
        )
        user_prompt = BATCH_USER_PROMPT_TEMPLATE.format(tweets_json=tweets_json)
        parsed = self._call_with_retry(user_prompt)
        return {r.tweet_id: r for r in parsed.results}

    def _classify_single(self, tweet: TweetData) -> ClassificationResult:
        """Classify a single tweet with retry + exponential backoff."""
        tweet_json = json.dumps(
            {"tweet_id": tweet.tweet_id, "text": tweet.text, "author": tweet.author_username},
            indent=2,
        )
        user_prompt = SINGLE_USER_PROMPT_TEMPLATE.format(tweet_json=tweet_json)
        parsed = self._call_with_retry(user_prompt)
        return parsed.results[0]

    def _call_with_retry(self, user_prompt: str) -> BatchClassificationResult:
        """Call OpenAI API with exponential backoff retry."""
        last_error: Exception | None = None

        for attempt in range(MAX_RETRIES):
            try:
                response = self.client.responses.parse(
                    model=self.model,
                    instructions=SYSTEM_PROMPT,
                    input=user_prompt,
                    text_format=BatchClassificationResult,
                )
                parsed = response.output_parsed
                if parsed is None:
                    raise RuntimeError("OpenAI returned no parsed output")
                return parsed
            except Exception as e:
                last_error = e
                if attempt < MAX_RETRIES - 1:
                    delay = BASE_DELAY * (2 ** attempt)
                    logger.warning("API call failed (attempt %d/%d), retrying in %.1fs: %s", attempt + 1, MAX_RETRIES, delay, e)
                    time.sleep(delay)

        raise last_error  # type: ignore[misc]
