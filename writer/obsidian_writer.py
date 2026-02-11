from pathlib import Path

from classifier.models import ClassificationResult
from fetcher.models import TweetData

from .templates import NOTE_TEMPLATE


class ObsidianWriter:
    def __init__(self, vault_path: str):
        self.base_path = Path(vault_path) / "TwitterLikes"

    def write_notes(
        self, tweets: list[TweetData], classifications: list[ClassificationResult]
    ) -> dict[str, int]:
        classification_map = {c.tweet_id: c for c in classifications}
        stats: dict[str, int] = {"written": 0, "skipped": 0}

        for tweet in tweets:
            cls = classification_map.get(tweet.tweet_id)
            if cls is None:
                stats["skipped"] += 1
                continue

            folder = self.base_path / cls.category
            folder.mkdir(parents=True, exist_ok=True)

            note_path = folder / f"{tweet.tweet_id}.md"
            if note_path.exists():
                stats["skipped"] += 1
                continue

            tags_str = ", ".join(f'"{t}"' for t in cls.tags)
            content = NOTE_TEMPLATE.format(
                title=cls.title.replace('"', '\\"'),
                category=cls.category,
                author=tweet.author_username,
                date_liked=tweet.created_at.strftime("%Y-%m-%d"),
                tweet_url=tweet.tweet_url,
                tags=tags_str,
                tweet_text=tweet.text,
            )

            note_path.write_text(content)
            stats["written"] += 1

        return stats
