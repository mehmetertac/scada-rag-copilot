"""Citation gate: every cause must cite a retrieved chunk verbatim."""

from __future__ import annotations

import re
from dataclasses import dataclass

from scada_rag.retrieve import Hit

NO_GROUNDED_CAUSE = "no grounded cause found"


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


@dataclass(frozen=True)
class GroundedCause:
    cause: str
    source: str
    quote: str
    supporting_signal: str


@dataclass(frozen=True)
class AgentAnswer:
    status: str  # "grounded" | "abstain" | "baseline"
    causes: tuple[GroundedCause, ...]
    next_check: str
    confidence: str
    message: str = ""

    @property
    def is_abstain(self) -> bool:
        return self.status == "abstain" or self.message == NO_GROUNDED_CAUSE


def abstain_answer(*, next_check: str = "", confidence: str = "none") -> AgentAnswer:
    return AgentAnswer(
        status="abstain",
        causes=(),
        next_check=next_check,
        confidence=confidence,
        message=NO_GROUNDED_CAUSE,
    )


def quote_in_hit(quote: str, hit: Hit) -> bool:
    q = normalize_whitespace(quote)
    if not q:
        return False
    body = normalize_whitespace(hit.text)
    return q in body


def filter_grounded_causes(
    raw_causes: list[dict[str, str]],
    hits: list[Hit],
) -> list[GroundedCause]:
    """Keep causes whose source matches a hit and quote is a substring of that hit."""
    by_source: dict[str, list[Hit]] = {}
    for h in hits:
        by_source.setdefault(h.source, []).append(h)
    kept: list[GroundedCause] = []
    for item in raw_causes:
        source = str(item.get("source", "")).strip()
        source_hits = by_source.get(source)
        if not source_hits:
            continue
        quote = str(item.get("quote", ""))
        if not any(quote_in_hit(quote, h) for h in source_hits):
            continue
        kept.append(
            GroundedCause(
                cause=str(item.get("cause", "")).strip(),
                source=source,
                quote=quote.strip(),
                supporting_signal=str(item.get("supporting_signal", "")).strip(),
            )
        )
    return kept


def build_agent_answer(
    raw_causes: list[dict[str, str]],
    hits: list[Hit],
    *,
    next_check: str,
    confidence: str,
) -> AgentAnswer:
    causes = filter_grounded_causes(raw_causes, hits)
    if not causes:
        return abstain_answer()
    return AgentAnswer(
        status="grounded",
        causes=tuple(causes),
        next_check=next_check.strip(),
        confidence=confidence.strip(),
    )
