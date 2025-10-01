from pydantic import BaseModel
from typing import List

class QuoteBase(BaseModel):
    text: str
    author: str
    tags: List[str]

class QuoteCreate(QuoteBase):
    url: str

class Quote(QuoteBase):
    id: int

    class Config:
        orm_mode = True

class ScrapeRequest(BaseModel):
    source: str = "all"
    mode: str = "static"
    max_articles: int = 50
