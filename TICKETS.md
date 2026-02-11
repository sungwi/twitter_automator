# Implementation Tickets

## Ticket 1: Project Scaffolding & Configuration
**Status**: Done
**Dependencies**: None
**Scope**:
- Create directory structure with all `__init__.py` files
- Create `requirements.txt` with all dependencies
- Create `config.yaml.example` and `.env.example`
- Implement `config.py` — load `.env` + `config.yaml`, merge with CLI args, return `AppConfig` dataclass
- Validate required keys based on mode (mock vs real)

**Files to create**:
- `requirements.txt`
- `config.yaml.example`
- `.env.example`
- `config.py`
- `fetcher/__init__.py`
- `classifier/__init__.py`
- `writer/__init__.py`

---

## Ticket 2: Data Models
**Status**: Done
**Dependencies**: None
**Scope**:
- `fetcher/models.py` — `TweetData` pydantic model (tweet_id, text, author_username, author_name, created_at, tweet_url, referenced_urls)
- `fetcher/base.py` — `TweetFetcher` protocol with `fetch_liked_tweets(since: date) -> list[TweetData]`
- `classifier/models.py` — `Category` literal type, `TweetClassification` model, `BatchClassificationResult` model

**Files to create**:
- `fetcher/models.py`
- `fetcher/base.py`
- `classifier/models.py`

---

## Ticket 3: Mock Twitter Client
**Status**: Done
**Dependencies**: Ticket 2 (needs TweetData model)
**Scope**:
- `fetcher/mock_client.py` — 20 realistic hardcoded tweets spread across 4 categories (5 each)
- Implements `TweetFetcher` protocol
- Filters by `since` date parameter
- Tweets should have realistic text, authors, dates (Jan-Feb 2026), and URLs

**Files to create**:
- `fetcher/mock_client.py`

---

## Ticket 4: OpenAI Classifier
**Status**: Done
**Dependencies**: Ticket 2 (needs classifier models)
**Scope**:
- `classifier/prompts.py` — system prompt with category definitions, batch user prompt builder
- `classifier/openai_classifier.py` — `OpenAIClassifier` class with:
  - `classify_tweets(tweets) -> dict[tweet_id, category]`
  - Batch processing (configurable batch size, default 10)
  - OpenAI structured outputs (json_schema response format)
  - Retry logic with exponential backoff
  - Fallback to individual classification on batch failure
  - Unclassifiable tweets default to "others"

**Files to create**:
- `classifier/prompts.py`
- `classifier/openai_classifier.py`

---

## Ticket 5: Obsidian Writer
**Status**: Done
**Dependencies**: Ticket 2 (needs TweetData and Category models)
**Scope**:
- `writer/templates.py` — note template (YAML frontmatter + markdown body), dashboard template (Dataview queries)
- `writer/obsidian_writer.py` — `ObsidianWriter` class:
  - `setup_folders()` — create `TwitterLikes/{Books,Articles_News,Items_of_Interest,Others}/`
  - `write_tweet_note(tweet, category)` — write `{tweet_id}.md` with frontmatter, skip if exists
- `writer/dashboard.py` — `DashboardWriter` class:
  - `write_dashboard()` — generate `TwitterLikes/Dashboard.md` with Dataview queries (summary, per-category tables, recent likes)

**Files to create**:
- `writer/templates.py`
- `writer/obsidian_writer.py`
- `writer/dashboard.py`

---

## Ticket 6: CLI Entry Point & Pipeline Orchestration
**Status**: Done
**Dependencies**: Tickets 1, 3, 4, 5 (needs all modules)
**Scope**:
- `main.py` — argparse CLI with flags: `--since`, `--vault-path`, `--mock`, `--batch-size`, `--verbose`
- Pipeline: load config → fetch tweets → classify → write notes → write dashboard → print summary
- Select mock vs real fetcher based on `--mock` flag
- Logging setup based on `--verbose`

**Files to create**:
- `main.py`

---

## Ticket 7: Real Twitter Client
**Status**: Done
**Dependencies**: Ticket 2 (needs TweetData model)
**Scope**:
- `fetcher/twitter_client.py` — `TwitterClient` class using tweepy:
  - OAuth 1.0a User Context authentication
  - `get_liked_tweets` with pagination via `tweepy.Paginator`
  - Request `tweet_fields`, `expansions`, `user_fields` for full data
  - Filter by `since` date (compare against `created_at`)
  - Extract URLs from tweet entities
  - Handle auth errors, rate limits, network errors

**Files to create**:
- `fetcher/twitter_client.py`

---

## Dependency Graph

```
Ticket 1 (Scaffolding) ──┐
                          ├──→ Ticket 6 (CLI/Pipeline)
Ticket 2 (Models) ───┬───┤
                      │   │
                      ├──→ Ticket 3 (Mock Client) ──→ Ticket 6
                      ├──→ Ticket 4 (Classifier) ───→ Ticket 6
                      ├──→ Ticket 5 (Obsidian Writer) → Ticket 6
                      └──→ Ticket 7 (Real Twitter Client)
```

**Parallel Group A** (no dependencies): Tickets 1, 2
**Parallel Group B** (after Group A): Tickets 3, 4, 5, 7
**Final** (after Group B): Ticket 6
