"""Knowledge-base loading: headings, front matter, metadata."""

from __future__ import annotations

from scada_rag.kb_loader import load_kb, split_sections


def test_split_sections_keeps_overview_and_skips_empty() -> None:
    sections = split_sections("# Title\n\nIntro line.\n\n## First\n\nBody.\n\n## Blank\n\n")
    assert sections == [("Overview", "# Title\n\nIntro line."), ("First", "Body.")]


def test_load_kb_metadata_and_nonempty_text(fixture_kb) -> None:
    documents = load_kb(fixture_kb)
    assert documents
    assert all(doc.text.strip() for doc in documents)

    gearbox = [doc for doc in documents if doc.metadata["source"] == "gearbox.md"]
    sections = {doc.metadata["section"] for doc in gearbox}
    assert "Symptoms in SCADA" in sections
    assert "Likely causes" in sections
    sample = gearbox[0]
    assert sample.metadata["doc_title"] == "Gearbox HSS bearing over-temperature"
    assert sample.metadata["component"] == "gearbox"
    assert sample.metadata["doc_type"] == "fault"
    assert sample.metadata["tags"] == "bearing, hss"
    assert "Gearbox HSS bearing over-temperature" in sample.text

    plain = [doc for doc in documents if doc.metadata["source"] == "plain.md"]
    assert plain
    assert plain[0].metadata["doc_title"] == "Notes without front matter"
    assert all(doc.metadata["section"] != "Blank" for doc in plain)
