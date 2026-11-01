"""Day-2 root-cause agent. Retrieval context is ready; chat completion is not."""

from __future__ import annotations

from scada_rag.config import RagConfig
from scada_rag.retrieve import Hit


def format_evidence(hits: list[Hit]) -> str:
    blocks: list[str] = []
    for rank, hit in enumerate(hits, start=1):
        blocks.append(f"[{rank}] {hit.doc_title} — {hit.section} ({hit.source})\n{hit.text}")
    return "\n\n".join(blocks)


def build_prompt(alarm_text: str, hits: list[Hit]) -> str:
    """Prompt for the day-2 chat model. Uses only retrieved sections as evidence."""
    evidence = format_evidence(hits) or "(no knowledge-base sections retrieved)"
    return (
        "You are a wind-turbine reliability assistant. Propose likely root causes "
        "for the SCADA alarm using only the evidence below. Rank the causes. "
        "Say when the evidence is insufficient. Do not invent OEM trip setpoints. "
        "When a section asks for digital-twin evidence, name the residual or tag "
        "to request; do not claim you queried the twin.\n\n"
        f"Alarm:\n{alarm_text.strip()}\n\n"
        f"Evidence:\n{evidence}\n"
    )


class RootCauseAgent:
    """Reads an alarm, retrieves manual sections, and (from day 2) proposes causes.

    ``propose`` is intentionally unimplemented until a local Ollama model is
    available. ``build_prompt`` plus :func:`scada_rag.retrieve.retrieve` is the
    supported day-1 path.
    """

    def __init__(self, config: RagConfig) -> None:
        self.config = config

    def propose(self, alarm_text: str, *, top_k: int | None = None) -> str:
        raise NotImplementedError(
            "Chat completion is day 2. Install Ollama and run "
            f"`ollama pull {self.config.ollama_model}`, then complete "
            "RootCauseAgent.propose with llama-index-llms-ollama. "
            "Until then, call retrieve() and build_prompt(). "
            f"Received alarm length {len(alarm_text.strip())}, top_k={top_k}."
        )
