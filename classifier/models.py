from typing import Literal

from pydantic import BaseModel

Category = Literal["Books", "Articles_News", "Items_of_Interest", "Others"]


class ClassificationResult(BaseModel):
    tweet_id: str
    category: Category
    title: str
    tags: list[str]


class BatchClassificationResult(BaseModel):
    results: list[ClassificationResult]
