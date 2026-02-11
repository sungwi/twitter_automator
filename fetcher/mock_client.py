from datetime import date, datetime, timezone

from .models import TweetData


MOCK_TWEETS: list[TweetData] = [
    # --- Books (5) ---
    TweetData(
        tweet_id="1001",
        text="Just finished 'Thinking, Fast and Slow' by Daniel Kahneman. Absolutely mind-blowing exploration of cognitive biases. A must-read for anyone interested in decision making.",
        author_username="bookworm42",
        author_name="Sarah Chen",
        created_at=datetime(2026, 1, 15, 10, 30, tzinfo=timezone.utc),
        tweet_url="https://x.com/bookworm42/status/1001",
        referenced_urls=["https://www.goodreads.com/book/show/11468377"],
    ),
    TweetData(
        tweet_id="1002",
        text="📚 'The Pragmatic Programmer' by Hunt & Thomas should be mandatory reading for every software engineer. The tips on DRY and orthogonality changed how I write code.",
        author_username="dev_reads",
        author_name="Marcus Dev",
        created_at=datetime(2026, 1, 18, 14, 0, tzinfo=timezone.utc),
        tweet_url="https://x.com/dev_reads/status/1002",
    ),
    TweetData(
        tweet_id="1003",
        text="Halfway through 'Sapiens' by Yuval Noah Harari. The agricultural revolution chapter completely reframed how I think about human progress. Highly recommend.",
        author_username="historynut",
        author_name="Lisa Park",
        created_at=datetime(2026, 1, 20, 9, 15, tzinfo=timezone.utc),
        tweet_url="https://x.com/historynut/status/1003",
    ),
    TweetData(
        tweet_id="1004",
        text="New release: 'System Design Interview Vol 2' by Alex Xu is out. Covers distributed systems patterns really well. Link: https://example.com/sdi2",
        author_username="techbooks",
        author_name="Tech Books Daily",
        created_at=datetime(2026, 2, 1, 8, 0, tzinfo=timezone.utc),
        tweet_url="https://x.com/techbooks/status/1004",
        referenced_urls=["https://example.com/sdi2"],
    ),
    TweetData(
        tweet_id="1005",
        text="If you haven't read 'Designing Data-Intensive Applications' by Martin Kleppmann, you're missing out. Best technical book I've read in years.",
        author_username="backend_eng",
        author_name="James Morrison",
        created_at=datetime(2026, 2, 3, 16, 45, tzinfo=timezone.utc),
        tweet_url="https://x.com/backend_eng/status/1005",
    ),
    # --- Articles / News (5) ---
    TweetData(
        tweet_id="2001",
        text="Great deep-dive on how Figma scaled their multiplayer infrastructure. Real-time collaboration at this scale is fascinating. https://example.com/figma-infra",
        author_username="techcrunch",
        author_name="TechCrunch",
        created_at=datetime(2026, 1, 12, 11, 0, tzinfo=timezone.utc),
        tweet_url="https://x.com/techcrunch/status/2001",
        referenced_urls=["https://example.com/figma-infra"],
    ),
    TweetData(
        tweet_id="2002",
        text="OpenAI announces GPT-5 with improved reasoning capabilities. Early benchmarks show 40% improvement on complex math problems. https://example.com/gpt5-announce",
        author_username="ai_news",
        author_name="AI News Hub",
        created_at=datetime(2026, 1, 25, 15, 30, tzinfo=timezone.utc),
        tweet_url="https://x.com/ai_news/status/2002",
        referenced_urls=["https://example.com/gpt5-announce"],
    ),
    TweetData(
        tweet_id="2003",
        text="Interesting article on why startups are moving away from microservices back to monoliths. The pendulum swings again. https://example.com/monolith-return",
        author_username="swengineer",
        author_name="Software Engineering Weekly",
        created_at=datetime(2026, 1, 28, 9, 0, tzinfo=timezone.utc),
        tweet_url="https://x.com/swengineer/status/2003",
        referenced_urls=["https://example.com/monolith-return"],
    ),
    TweetData(
        tweet_id="2004",
        text="Rust is now the second most-used language at Google after C++, surpassing Go for systems programming. Full report here: https://example.com/google-rust",
        author_username="devnews",
        author_name="Dev News",
        created_at=datetime(2026, 2, 2, 12, 0, tzinfo=timezone.utc),
        tweet_url="https://x.com/devnews/status/2004",
        referenced_urls=["https://example.com/google-rust"],
    ),
    TweetData(
        tweet_id="2005",
        text="The EU's new AI Act enforcement begins next month. Here's what developers need to know about compliance. Thread 🧵 https://example.com/eu-ai-act",
        author_username="policy_tech",
        author_name="Tech Policy Watch",
        created_at=datetime(2026, 2, 5, 8, 30, tzinfo=timezone.utc),
        tweet_url="https://x.com/policy_tech/status/2005",
        referenced_urls=["https://example.com/eu-ai-act"],
    ),
    # --- Items of Interest (5) ---
    TweetData(
        tweet_id="3001",
        text="This mechanical keyboard with an e-ink display on each keycap is wild. Fully programmable and the battery lasts 6 months. https://example.com/eink-keyboard",
        author_username="gadgetflow",
        author_name="Gadget Flow",
        created_at=datetime(2026, 1, 14, 10, 0, tzinfo=timezone.utc),
        tweet_url="https://x.com/gadgetflow/status/3001",
        referenced_urls=["https://example.com/eink-keyboard"],
    ),
    TweetData(
        tweet_id="3002",
        text="Found an amazing open-source tool for local-first AI: Ollama now supports vision models. Run multimodal AI completely offline. https://ollama.com",
        author_username="opensource_fan",
        author_name="Open Source Daily",
        created_at=datetime(2026, 1, 22, 13, 0, tzinfo=timezone.utc),
        tweet_url="https://x.com/opensource_fan/status/3002",
        referenced_urls=["https://ollama.com"],
    ),
    TweetData(
        tweet_id="3003",
        text="This 3D-printed desk organizer with built-in wireless charging is genius. STL files are free on Printables. https://example.com/desk-organizer",
        author_username="maker_space",
        author_name="Maker Space",
        created_at=datetime(2026, 1, 30, 17, 0, tzinfo=timezone.utc),
        tweet_url="https://x.com/maker_space/status/3003",
        referenced_urls=["https://example.com/desk-organizer"],
    ),
    TweetData(
        tweet_id="3004",
        text="Obsidian plugin of the week: 'Canvas Groups' lets you create visual clusters of notes with auto-layout. Game changer for project planning.",
        author_username="obsidian_tips",
        author_name="Obsidian Tips",
        created_at=datetime(2026, 2, 4, 11, 0, tzinfo=timezone.utc),
        tweet_url="https://x.com/obsidian_tips/status/3004",
    ),
    TweetData(
        tweet_id="3005",
        text="NASA's new James Webb image of the Crab Nebula is absolutely stunning. The level of detail is unprecedented. Full res: https://example.com/jwst-crab",
        author_username="space_pics",
        author_name="Space Photography",
        created_at=datetime(2026, 2, 6, 9, 30, tzinfo=timezone.utc),
        tweet_url="https://x.com/space_pics/status/3005",
        referenced_urls=["https://example.com/jwst-crab"],
    ),
    # --- Others (5) ---
    TweetData(
        tweet_id="4001",
        text="Monday mood: coffee hasn't kicked in yet and I already have 47 unread Slack messages 😅",
        author_username="dev_humor",
        author_name="Dev Humor",
        created_at=datetime(2026, 1, 13, 8, 0, tzinfo=timezone.utc),
        tweet_url="https://x.com/dev_humor/status/4001",
    ),
    TweetData(
        tweet_id="4002",
        text="Hot take: tabs are superior to spaces and I will die on this hill. Fight me in the replies.",
        author_username="code_opinions",
        author_name="Hot Code Takes",
        created_at=datetime(2026, 1, 19, 12, 0, tzinfo=timezone.utc),
        tweet_url="https://x.com/code_opinions/status/4002",
    ),
    TweetData(
        tweet_id="4003",
        text="Just adopted a rescue cat named Null. Every database joke writes itself now. 🐱",
        author_username="dev_life",
        author_name="Developer Life",
        created_at=datetime(2026, 1, 26, 18, 0, tzinfo=timezone.utc),
        tweet_url="https://x.com/dev_life/status/4003",
    ),
    TweetData(
        tweet_id="4004",
        text="Celebrating 5 years at my company today! 🎉 Grateful for the incredible team and all the growth. Here's to more!",
        author_username="career_dev",
        author_name="Career Developer",
        created_at=datetime(2026, 2, 1, 14, 0, tzinfo=timezone.utc),
        tweet_url="https://x.com/career_dev/status/4004",
    ),
    TweetData(
        tweet_id="4005",
        text="The sunset from my home office window today was unreal. Sometimes WFH has its perks. 🌅",
        author_username="remote_worker",
        author_name="Remote Life",
        created_at=datetime(2026, 2, 7, 17, 30, tzinfo=timezone.utc),
        tweet_url="https://x.com/remote_worker/status/4005",
    ),
]


class MockTweetFetcher:
    def fetch_liked_tweets(self, since: date | None = None) -> list[TweetData]:
        if since is None:
            return list(MOCK_TWEETS)
        return [t for t in MOCK_TWEETS if t.created_at.date() >= since]
