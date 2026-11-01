"""Top-k retrieval with document title and section metadata."""

from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass
from pathlib import Path

from llama_index.core import VectorStoreIndex

from scada_rag.config import RagConfig
from scada_rag.embeddings import build_embed_model
from scada_rag.store import collection_count, open_vector_store

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Hit:
    score: float
    doc_title: str
    section: str
    source: str
    text: str
    component: str
    doc_type: str


def retrieve(query: str, config: RagConfig, *, top_k: int | None = None) -> list[Hit]:
    """Return the top-k chunks for ``query``. Requires a prior :func:`ingest`."""
    k = top_k if top_k is not None else config.top_k
    if k < 1:
        raise ValueError("top_k must be >= 1")

    embed_model = build_embed_model(config)
    try:
        vector_store = open_vector_store(config.persist_dir, config.collection, reset=False)
    except Exception as exc:
        raise FileNotFoundError(
            f"No collection {config.collection!r} in {config.persist_dir}. Run ingest first."
        ) from exc
    if collection_count(vector_store) == 0:
        raise FileNotFoundError(
            f"Collection {config.collection!r} in {config.persist_dir} is empty. Run ingest first."
        )

    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)
    nodes = index.as_retriever(similarity_top_k=k).retrieve(query)
    hits: list[Hit] = []
    for node in nodes:
        source_node = node.node
        meta = source_node.metadata or {}
        hits.append(
            Hit(
                score=float(node.score or 0.0),
                doc_title=str(meta.get("doc_title", "")),
                section=str(meta.get("section", "")),
                source=str(meta.get("source", "")),
                text=source_node.get_content(),
                component=str(meta.get("component", "")),
                doc_type=str(meta.get("doc_type", "")),
            )
        )
    logger.info("Retrieved %s hits for query", len(hits))
    return hits


def format_hits(hits: list[Hit]) -> str:
    if not hits:
        return "No hits."
    blocks: list[str] = []
    for rank, hit in enumerate(hits, start=1):
        preview = " ".join(hit.text.split())
        if len(preview) > 280:
            preview = preview[:277] + "..."
        blocks.append(
            f"{rank}. score={hit.score:.3f}  {hit.doc_title} / {hit.section}  [{hit.source}]\n"
            f"   {preview}"
        )
    return "\n".join(blocks)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Retrieve knowledge-base chunks for an alarm query."
    )
    parser.add_argument("--query", required=True)
    parser.add_argument("--top-k", type=int, default=None)
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--embed-mode", choices=["huggingface", "mock"], default=None)
    parser.add_argument("--persist-dir", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    args = build_parser().parse_args(argv)
    config = RagConfig.load(
        path=args.config,
        embed_mode=args.embed_mode,
        persist_dir=args.persist_dir,
    )
    try:
        hits = retrieve(args.query, config, top_k=args.top_k)
    except FileNotFoundError as exc:
        print(exc)
        return 2
    print(format_hits(hits))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
