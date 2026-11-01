"""Ingest with the offline hash embedder."""

from __future__ import annotations

from scada_rag.config import RagConfig
from scada_rag.ingest import ingest
from scada_rag.retrieve import retrieve


def _config(tmp_path, fixture_kb) -> RagConfig:
    return RagConfig.load(
        embed_mode="mock",
        persist_dir=tmp_path / "chroma",
        kb_dir=fixture_kb,
    )


def test_ingest_persists_and_is_idempotent(tmp_path, fixture_kb) -> None:
    config = _config(tmp_path, fixture_kb)
    first = ingest(config)
    second = ingest(config)
    assert first > 0
    assert second == first


def test_ingested_chunks_keep_section_metadata(tmp_path, fixture_kb) -> None:
    config = _config(tmp_path, fixture_kb)
    ingest(config)
    hits = retrieve("HSS bearing temperature", config, top_k=3)
    assert hits
    assert all(hit.doc_title for hit in hits)
    assert all(hit.section for hit in hits)
    assert all(hit.source.endswith(".md") for hit in hits)
