"""Rebuild the index, run the five day-1 queries, write ``results/sanity_queries.md``."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scada_rag.config import RagConfig  # noqa: E402
from scada_rag.ingest import ingest  # noqa: E402
from scada_rag.retrieve import retrieve  # noqa: E402
from scada_rag.sanity import SANITY_QUERIES, render_report  # noqa: E402


def main() -> int:
    config = RagConfig.load()
    count = ingest(config)
    print(f"Ingested {count} chunks into {config.persist_dir}")
    rows = []
    failed = 0
    for query, expected in SANITY_QUERIES:
        hits = retrieve(query, config, top_k=3)
        sources = [hit.source for hit in hits]
        if expected not in sources:
            failed += 1
        rows.append((query, expected, hits))
        print(f"{'PASS' if expected in sources else 'FAIL'}  {query}")
        for hit in hits:
            print(f"    {hit.score:.3f}  {hit.source}  /  {hit.section}")

    report = render_report(config, rows)
    out = ROOT / "results" / "sanity_queries.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(f"Wrote {out}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
