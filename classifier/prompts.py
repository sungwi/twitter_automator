SYSTEM_PROMPT = """\
You are a tweet classifier. Classify each tweet into exactly one category:

- **Books**: Tweets about books — recommendations, reviews, reading lists, quotes from books, book launches.
- **Articles_News**: Tweets linking to or discussing articles, blog posts, news stories, research papers, industry reports.
- **Items_of_Interest**: Tweets about interesting tools, products, gadgets, open-source projects, plugins, visual media, or other notable discoveries.
- **Others**: Personal updates, humor, opinions, memes, celebrations, or anything that doesn't fit the above categories.

For each tweet, also provide:
- A short descriptive **title** (max 10 words) summarizing the content.
- 1-3 relevant **tags** (lowercase, no spaces — use underscores).

If a tweet is ambiguous or unclassifiable, default to "Others".\
"""

BATCH_USER_PROMPT_TEMPLATE = """\
Classify each of the following tweets. Return a JSON object with a "results" array containing one entry per tweet.

Tweets:
{tweets_json}\
"""

SINGLE_USER_PROMPT_TEMPLATE = """\
Classify this tweet. Return a JSON object with a "results" array containing one entry.

Tweet:
{tweet_json}\
"""
