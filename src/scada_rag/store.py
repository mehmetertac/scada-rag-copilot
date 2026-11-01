"""Persistent Chroma collection used by ingest and retrieve."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from chromadb.config import Settings
from llama_index.vector_stores.chroma import ChromaVectorStore

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")


class PrecomputedEmbeddingFunction(EmbeddingFunction[Documents]):
    """Keep Chroma from downloading its default ONNX embedder.

    llama-index always passes vectors into ``collection.add``. This function
    must not be called.
    """

    def __init__(self) -> None:
        return

    def __call__(self, input: Documents) -> Embeddings:
        raise RuntimeError("Embeddings are computed outside Chroma")

    @staticmethod
    def name() -> str:
        return "precomputed"

    def get_config(self) -> dict[str, Any]:
        return {}

    @staticmethod
    def build_from_config(config: dict[str, Any]) -> PrecomputedEmbeddingFunction:
        del config
        return PrecomputedEmbeddingFunction()

    def default_space(self) -> str:
        return "cosine"


def open_vector_store(persist_dir: Path, collection_name: str, *, reset: bool) -> ChromaVectorStore:
    persist_dir.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(
        path=str(persist_dir),
        settings=Settings(anonymized_telemetry=False),
    )
    if reset:
        names: set[str] = set()
        for item in client.list_collections():
            # chromadb has returned either names or Collection objects.
            names.add(item if isinstance(item, str) else item.name)
        if collection_name in names:
            client.delete_collection(collection_name)
        collection = client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
            embedding_function=PrecomputedEmbeddingFunction(),
        )
    else:
        collection = client.get_collection(
            name=collection_name,
            embedding_function=PrecomputedEmbeddingFunction(),
        )
    return ChromaVectorStore(chroma_collection=collection)


def collection_count(vector_store: ChromaVectorStore) -> int:
    return int(vector_store._collection.count())
