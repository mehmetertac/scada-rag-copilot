"""Retrieval against the real bge-small model and the real knowledge base."""

from __future__ import annotations

import pytest

from scada_rag.config import RagConfig, repo_root
from scada_rag.ingest import ingest
from scada_rag.retrieve import retrieve
from scada_rag.sanity import SANITY_QUERIES


@pytest.mark.integration
def test_sanity_queries_return_expected_doc(tmp_path) -> None:
    config = RagConfig.load(
        embed_mode="huggingface",
        persist_dir=tmp_path / "chroma",
        kb_dir=repo_root() / "kb",
    )
    count = ingest(config)
    assert count > 0

    misses: list[str] = []
    for query, expected in SANITY_QUERIES:
        hits = retrieve(query, config, top_k=3)
        sources = [hit.source for hit in hits]
        if expected not in sources:
            misses.append(f"{query!r} -> {sources}, expected {expected}")
    assert not misses, "\n".join(misses)
