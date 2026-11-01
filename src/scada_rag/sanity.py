"""The five day-1 retrieval checks. Shared by the script and the integration test."""

from __future__ import annotations

from scada_rag.config import RagConfig
from scada_rag.retrieve import Hit

SANITY_QUERIES: tuple[tuple[str, str], ...] = (
    (
        "gearbox HSS bearing temp rising at partial load",
        "gearbox_hss_bearing_overtemp.md",
    ),
    (
        "gearbox oil temperature high but bearing normal",
        "gearbox_oil_overtemp.md",
    ),
    (
        "pitch angle deviation alarm blade 2",
        "pitch_system_errors.md",
    ),
    (
        "generator NDE bearing temperature trend",
        "generator_bearing_faults.md",
    ),
    (
        "when to stop the turbine for a gearbox temperature alarm",
        "procedure_escalation_thresholds.md",
    ),
)


def render_report(config: RagConfig, rows: list[tuple[str, str, list[Hit]]]) -> str:
    """Markdown report. Each row is (query, expected source file, top hits)."""
    lines = [
        "# Sanity queries",
        "",
        f"Embed model: `{config.embed_model}` (`{config.embed_mode}`).",
        f"Chunk size {config.chunk_size}, overlap {config.chunk_overlap}, top-k checked: 3.",
        "",
        "A query passes when the expected source file is in the top 3.",
        "",
    ]
    passed = 0
    for index, (query, expected, hits) in enumerate(rows, start=1):
        sources = [hit.source for hit in hits]
        ok = expected in sources
        passed += int(ok)
        lines.append(f"## {index}. {query}")
        lines.append("")
        lines.append(f"Expected: `{expected}`. Result: **{'pass' if ok else 'fail'}**.")
        lines.append("")
        lines.append("| Rank | Score | Source | Section |")
        lines.append("| --- | --- | --- | --- |")
        if not hits:
            lines.append("| — | — | — | — |")
        for rank, hit in enumerate(hits, start=1):
            title = hit.section.replace("|", "/")
            lines.append(f"| {rank} | {hit.score:.3f} | `{hit.source}` | {title} |")
        lines.append("")
    lines.append(f"Passed {passed} of {len(rows)}.")
    lines.append("")
    return "\n".join(lines)
