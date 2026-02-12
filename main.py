import argparse
import logging
import sys
from datetime import date

from config import AppConfig, ConfigError, load_config, validate_config
from fetcher import MockTweetFetcher, TwitterFetcher
from classifier import OpenAIClassifier
from writer import ObsidianWriter, DashboardWriter


def parse_args() -> dict:
    parser = argparse.ArgumentParser(description="Twitter Likes → Obsidian Dashboard")
    parser.add_argument("--since", type=str, help="Only process tweets after this date (YYYY-MM-DD)")
    parser.add_argument("--vault-path", type=str, help="Path to Obsidian vault")
    parser.add_argument("--mock", action="store_true", help="Use mock tweet data")
    parser.add_argument("--batch-size", type=int, default=None, help="Tweets per OpenAI API call")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--model", type=str, default=None, help="OpenAI model to use (default: gpt-4o-mini)")
    args = parser.parse_args()
    return {
        "since": args.since,
        "vault_path": args.vault_path,
        "mock": args.mock,
        "batch_size": args.batch_size,
        "verbose": args.verbose,
        "openai_model": args.model,
    }


def setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def run(config: AppConfig) -> None:
    since_date: date | None = None
    if config.since:
        since_date = date.fromisoformat(config.since)

    # 1. Fetch tweets
    if config.mock:
        fetcher = MockTweetFetcher()
        print("[Fetcher] Using mock data")
    else:
        fetcher = TwitterFetcher(
            consumer_key=config.twitter_consumer_key,
            consumer_secret=config.twitter_consumer_secret,
            access_token=config.twitter_access_token,
            access_token_secret=config.twitter_access_token_secret,
        )
        print("[Fetcher] Using Twitter API (OAuth 1.0a)")

    tweets = fetcher.fetch_liked_tweets(since=since_date)
    print(f"[Fetcher] Fetched {len(tweets)} tweets")

    if not tweets:
        print("No tweets to process. Done.")
        return

    # 2. Classify tweets
    classifier = OpenAIClassifier(api_key=config.openai_api_key, model=config.openai_model, batch_size=config.batch_size)
    print(f"[Classifier] Classifying {len(tweets)} tweets (batch size: {config.batch_size})")
    classifications = classifier.classify_tweets(tweets)
    print(f"[Classifier] Classified {len(classifications)} tweets")

    if config.verbose:
        for tweet_id, c in classifications.items():
            print(f"  {tweet_id}: {c.category} — {c.title}")

    # 3. Write Obsidian notes
    writer = ObsidianWriter(config.vault_path)
    stats = writer.write_notes(tweets, list(classifications.values()))
    print(f"[Writer] Written: {stats['written']}, Skipped: {stats['skipped']}")

    # 4. Write dashboard
    dashboard_writer = DashboardWriter(config.vault_path)
    dashboard_path = dashboard_writer.write_dashboard()
    print(f"[Dashboard] Generated at {dashboard_path}")

    print("\nDone!")


def main() -> None:
    cli_args = parse_args()
    config = load_config(cli_args)
    setup_logging(config.verbose)

    try:
        validate_config(config)
    except ConfigError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    run(config)


if __name__ == "__main__":
    main()
