from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Chunk:
    text: str
    source: str
    score: Optional[float] = None

@dataclass
class Question:
    text: str
    conversation_id: Optional[str] = None

@dataclass
class Answer:
    text: str
    sources: List[str]
    chunks: List[Chunk]
    stats: Optional[dict] = None