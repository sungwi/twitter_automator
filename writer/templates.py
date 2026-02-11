NOTE_TEMPLATE = """\
---
title: "{title}"
category: "{category}"
author: "@{author}"
date_liked: {date_liked}
tweet_url: "{tweet_url}"
tags: [{tags}]
---

# {title}

> {tweet_text}

**Author**: [@{author}](https://x.com/{author})
**Tweet**: [{tweet_url}]({tweet_url})
**Date**: {date_liked}
"""


DASHBOARD_TEMPLATE = """\
---
cssclasses: [wide-page]
---

# Twitter Likes Dashboard

## Summary

```dataview
TABLE length(rows) AS Count
FROM "TwitterLikes"
WHERE category
GROUP BY category
SORT length(rows) DESC
```

## Recent Likes

```dataview
TABLE title, category, author, date_liked
FROM "TwitterLikes"
WHERE category
SORT date_liked DESC
LIMIT 20
```

## Books

```dataview
TABLE title, author, date_liked, tags
FROM "TwitterLikes/Books"
SORT date_liked DESC
```

## Articles & News

```dataview
TABLE title, author, date_liked, tags
FROM "TwitterLikes/Articles_News"
SORT date_liked DESC
```

## Items of Interest

```dataview
TABLE title, author, date_liked, tags
FROM "TwitterLikes/Items_of_Interest"
SORT date_liked DESC
```

## Others

```dataview
TABLE title, author, date_liked, tags
FROM "TwitterLikes/Others"
SORT date_liked DESC
```
"""
