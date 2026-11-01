"""Embedding models: local bge-small, or a hash embedder for offline tests."""

from __future__ import annotations

import hashlib
import math
import os

from llama_index.core.base.embeddings.base import BaseEmbedding
from pydantic import Field

from scada_rag.config import RagConfig

os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")

_BGE_QUERY_INSTRUCTION = "Represent this sentence for searching relevant passages: "


class HashEmbedding(BaseEmbedding):
    """Deterministic unit vectors. Rankings are not semantic; tests only need a store."""

    embed_dim: int = Field(default=64)

    def __init__(self, embed_dim: int = 64, **kwargs: object) -> None:
        super().__init__(embed_dim=embed_dim, model_name="hash-mock", **kwargs)

    def _vector(self, text: str) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        values: list[float] = []
        seed = digest
        while len(values) < self.embed_dim:
            seed = hashlib.sha256(seed).digest()
            for byte in seed:
                values.append((byte / 127.5) - 1.0)
                if len(values) == self.embed_dim:
                    break
        norm = math.sqrt(sum(value * value for value in values)) or 1.0
        return [value / norm for value in values]

    def _get_text_embedding(self, text: str) -> list[float]:
        return self._vector(text)

    def _get_query_embedding(self, query: str) -> list[float]:
        return self._vector(query)

    async def _aget_text_embedding(self, text: str) -> list[float]:
        return self._get_text_embedding(text)

    async def _aget_query_embedding(self, query: str) -> list[float]:
        return self._get_query_embedding(query)


def build_embed_model(config: RagConfig) -> BaseEmbedding:
    if config.embed_mode == "mock":
        return HashEmbedding(embed_dim=64)
    if config.embed_mode != "huggingface":
        raise ValueError(f"Unknown embed_mode {config.embed_mode!r}")

    from llama_index.embeddings.huggingface import HuggingFaceEmbedding

    kwargs: dict[str, object] = {
        "model_name": config.embed_model,
        "device": "cpu",
        "trust_remote_code": False,
    }
    if "bge" in config.embed_model.lower():
        kwargs["query_instruction"] = _BGE_QUERY_INSTRUCTION
    return HuggingFaceEmbedding(**kwargs)
