import os
from dataclasses import dataclass
from pathlib import Path

import yaml
from dotenv import load_dotenv


@dataclass
class AppConfig:
    vault_path: str = ""
    twitter_bearer_token: str = ""
    twitter_consumer_key: str = ""
    twitter_consumer_secret: str = ""
    twitter_access_token: str = ""
    twitter_access_token_secret: str = ""
    openai_api_key: str = ""
    batch_size: int = 10
    verbose: bool = False
    mock: bool = False
    since: str | None = None


class ConfigError(Exception):
    pass


def validate_config(config: AppConfig) -> None:
    """Validate required keys based on mode (mock vs real)."""
    if not config.vault_path:
        raise ConfigError("vault_path is required (set via --vault-path, config.yaml, or VAULT_PATH env var)")

    if not config.openai_api_key:
        raise ConfigError("OPENAI_API_KEY is required (set in .env or environment)")

    if not config.mock:
        has_oauth = all([
            config.twitter_consumer_key,
            config.twitter_consumer_secret,
            config.twitter_access_token,
            config.twitter_access_token_secret,
        ])
        if not has_oauth:
            raise ConfigError(
                "Twitter OAuth 1.0a credentials required when not using --mock. "
                "Set TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, "
                "TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET in .env or environment."
            )


def load_config(cli_args: dict | None = None) -> AppConfig:
    """Load config with layered precedence: .env > config.yaml > CLI args."""
    # 1. Load .env file
    load_dotenv()

    # 2. Load config.yaml if it exists
    yaml_config: dict = {}
    config_path = Path("config.yaml")
    if config_path.exists():
        with open(config_path) as f:
            yaml_config = yaml.safe_load(f) or {}

    # 3. Build config: start with yaml, override with env, then CLI args
    config = AppConfig(
        vault_path=yaml_config.get("vault_path", ""),
        batch_size=yaml_config.get("batch_size", 10),
        verbose=yaml_config.get("verbose", False),
    )

    # Env vars override yaml
    if os.getenv("TWITTER_BEARER_TOKEN"):
        config.twitter_bearer_token = os.getenv("TWITTER_BEARER_TOKEN", "")
    if os.getenv("TWITTER_CONSUMER_KEY"):
        config.twitter_consumer_key = os.getenv("TWITTER_CONSUMER_KEY", "")
    if os.getenv("TWITTER_CONSUMER_SECRET"):
        config.twitter_consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET", "")
    if os.getenv("TWITTER_ACCESS_TOKEN"):
        config.twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN", "")
    if os.getenv("TWITTER_ACCESS_TOKEN_SECRET"):
        config.twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")
    if os.getenv("OPENAI_API_KEY"):
        config.openai_api_key = os.getenv("OPENAI_API_KEY", "")

    # CLI args override everything
    if cli_args:
        if cli_args.get("vault_path"):
            config.vault_path = cli_args["vault_path"]
        if cli_args.get("batch_size") is not None:
            config.batch_size = cli_args["batch_size"]
        if cli_args.get("verbose"):
            config.verbose = True
        if cli_args.get("mock"):
            config.mock = True
        if cli_args.get("since"):
            config.since = cli_args["since"]

    return config
