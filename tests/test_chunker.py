"""Tests del chunker. No requieren Ollama ni red."""

from pathlib import Path

import pytest

from agente_rag.chunker import Chunk, load_corpus, split_documents

CORPUS = Path(__file__).resolve().parents[1] / "base_conocimiento"


def test_load_corpus_returns_sixteen_docs():
    docs = load_corpus(CORPUS)
    assert len(docs) == 16
    assert all("name" in d and "text" in d for d in docs)
    # Verificar que están todos los archivos del corpus DNI
    names = {d["name"] for d in docs}
    assert "01_faq_dni.txt" in names
    assert "16_resis_49_preguntas.txt" in names


def test_load_corpus_missing_dir(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_corpus(tmp_path / "no-existe")


def test_split_documents_preserves_source():
    docs = load_corpus(CORPUS)
    chunks = split_documents(docs, chunk_size=500, chunk_overlap=100)

    assert len(chunks) > 50, "se esperan muchos chunks con 16 documentos"
    assert all(isinstance(c, Chunk) for c in chunks)
    assert all(c.source.endswith(".txt") for c in chunks)
    assert all(c.text and isinstance(c.text, str) for c in chunks)
    assert all(c.id.endswith(f"chunk_{c.chunk_index:04d}") for c in chunks)


def test_split_documents_chunk_size_bounded():
    docs = load_corpus(CORPUS)
    chunks = split_documents(docs, chunk_size=500, chunk_overlap=100)
    too_large = [c for c in chunks if len(c.text) > 600]
    assert not too_large, f"chunks demasiado grandes: {len(too_large)}"
