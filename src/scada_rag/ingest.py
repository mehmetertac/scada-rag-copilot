"""Chunk the knowledge base, embed it, and persist a Chroma index."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

from scada_rag.config import RagConfig
from scada_rag.embeddings import build_embed_model
from scada_rag.kb_loader import load_kb
from scada_rag.store import collection_count, open_vector_store

logger = logging.getLogger(__name__)


def chunk_documents(documents: list, config: RagConfig) -> list:
    splitter = SentenceSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
    )
    return splitter.get_nodes_from_documents(documents)


def ingest(config: RagConfig) -> int:
    """Rebuild the vector store from ``config.kb_dir``. Returns the node count."""
    documents = load_kb(config.kb_dir)
    nodes = chunk_documents(documents, config)
    if not nodes:
        raise RuntimeError(f"Chunking produced no nodes from {config.kb_dir}")

    embed_model = build_embed_model(config)
    vector_store = open_vector_store(config.persist_dir, config.collection, reset=True)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    VectorStoreIndex(
        nodes=nodes,
        storage_context=storage_context,
        embed_model=embed_model,
        show_progress=False,
    )
    count = collection_count(vector_store)
    logger.info("Ingested %s chunks into %s", count, config.persist_dir)
    return count


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Embed kb/ and persist a local Chroma index.")
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--embed-mode", choices=["huggingface", "mock"], default=None)
    parser.add_argument("--persist-dir", type=Path, default=None)
    parser.add_argument("--kb-dir", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    args = build_parser().parse_args(argv)
    config = RagConfig.load(
        path=args.config,
        embed_mode=args.embed_mode,
        persist_dir=args.persist_dir,
        kb_dir=args.kb_dir,
    )
    count = ingest(config)
    print(f"Ingested {count} chunks into {config.persist_dir} (collection {config.collection}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
