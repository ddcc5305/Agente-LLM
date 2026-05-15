"""Entidades de dominio — puro Python, sin dependencias externas."""

from dataclasses import dataclass, field
from typing import List, Optional


# Constante de dominio: frase literal de rechazo para preguntas fuera de ámbito
REJECTION_PHRASE = "No tengo esa información en mis fuentes"


@dataclass
class Chunk:
    """Fragmento de texto recuperado del corpus."""
    text: str
    source: str
    score: Optional[float] = None


@dataclass
class Question:
    """Pregunta formulada por el usuario."""
    text: str
    conversation_id: Optional[str] = None


@dataclass
class GenerationResult:
    """Resultado devuelto por un LLM: texto generado + métricas."""
    text: str
    stats: dict = field(default_factory=dict)


@dataclass
class Answer:
    """Respuesta completa del agente al usuario."""
    text: str
    sources: List[str]
    chunks: List[Chunk]
    stats: Optional[dict] = None