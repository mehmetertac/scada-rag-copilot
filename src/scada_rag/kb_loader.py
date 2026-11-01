"""Read ``kb/*.md`` into llama-index documents, one per ``##`` section."""

from __future__ import annotations

import re
from pathlib import Path

import yaml
from llama_index.core import Document

_FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_H1 = re.compile(r"(?m)^#\s+(.+?)\s*$")
_METADATA_KEYS = ("doc_title", "section", "component", "doc_type", "tags", "source")


def _as_tags(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return str(value)


def _title_from_body(body: str, fallback: str) -> str:
    match = _H1.search(body)
    if match:
        return match.group(1).strip()
    return fallback


def split_sections(text: str) -> list[tuple[str, str]]:
    """Split markdown on ``##`` headings. Leading text is the Overview section."""
    parts = re.split(r"(?m)^##\s+", text)
    sections: list[tuple[str, str]] = []
    intro = parts[0].strip()
    if intro:
        sections.append(("Overview", intro))
    for part in parts[1:]:
        heading, _, body = part.partition("\n")
        heading = heading.strip()
        body = body.strip()
        if heading and body:
            sections.append((heading, body))
    return sections


def load_kb(kb_dir: Path) -> list[Document]:
    paths = sorted(path for path in kb_dir.glob("*.md") if path.is_file())
    if not paths:
        raise FileNotFoundError(f"No markdown files in {kb_dir}")

    documents: list[Document] = []
    for path in paths:
        raw = path.read_text(encoding="utf-8")
        meta: dict[str, object] = {}
        match = _FRONT_MATTER.match(raw)
        body = raw
        if match:
            loaded = yaml.safe_load(match.group(1)) or {}
            if not isinstance(loaded, dict):
                raise ValueError(f"Front matter in {path.name} must be a mapping")
            meta = loaded
            body = raw[match.end() :]

        title = str(meta.get("title") or _title_from_body(body, path.stem))
        component = str(meta.get("component") or "")
        doc_type = str(meta.get("doc_type") or "")
        tags = _as_tags(meta.get("tags"))

        for section, section_body in split_sections(body):
            text = f"{title}\n{section}\n\n{section_body}"
            metadata = {
                "doc_title": title,
                "section": section,
                "component": component,
                "doc_type": doc_type,
                "tags": tags,
                "source": path.name,
            }
            documents.append(
                Document(
                    text=text,
                    metadata=metadata,
                    excluded_embed_metadata_keys=list(_METADATA_KEYS),
                    excluded_llm_metadata_keys=list(_METADATA_KEYS),
                )
            )
    return documents
