"""Root-cause agent: retrieve, prompt, JSON answer, citation gate."""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from typing import Any

from scada_rag.alarms import AlarmPayload, format_alarm_text, formulate_query
from scada_rag.config import RagConfig
from scada_rag.grounding import (
    NO_GROUNDED_CAUSE,
    AgentAnswer,
    abstain_answer,
    build_agent_answer,
)
from scada_rag.retrieve import Hit, retrieve

Completer = Callable[[str], str]


def format_evidence(hits: list[Hit]) -> str:
    blocks: list[str] = []
    for rank, hit in enumerate(hits, start=1):
        blocks.append(f"[{rank}] {hit.doc_title} — {hit.section} ({hit.source})\n{hit.text}")
    return "\n\n".join(blocks)


def build_prompt(
    alarm_text: str,
    hits: list[Hit],
    *,
    use_retrieval: bool = True,
) -> str:
    """Prompt for the chat model. Uses only retrieved sections as evidence when enabled."""
    if use_retrieval and hits:
        evidence = format_evidence(hits)
    elif use_retrieval:
        evidence = "(no knowledge-base sections retrieved)"
    else:
        evidence = "(retrieval disabled — do not cite knowledge-base files you were not shown)"

    allowed_sources = ", ".join(sorted({h.source for h in hits})) if hits else "none"

    return (
        "You are a wind-turbine reliability assistant. Propose likely root causes "
        "for the SCADA alarm using ONLY the evidence below when it is present. "
        "Respond with a single JSON object, no markdown fences, with keys:\n"
        '  "causes": list of objects, each with "cause", "source" (kb filename only, '
        f'must be one of: {allowed_sources}), "quote" (exact substring from that chunk), '
        '"supporting_signal" (SCADA tag from the alarm that supports the cause),\n'
        '  "next_check": string,\n'
        '  "confidence": "high" | "medium" | "low".\n'
        "Rank causes most likely first. If evidence is insufficient, return "
        '{"causes": [], "next_check": "...", "confidence": "low"}.\n'
        "Do not invent OEM trip setpoints. Do not claim you queried the digital twin.\n\n"
        f"Alarm:\n{alarm_text.strip()}\n\n"
        f"Evidence:\n{evidence}\n"
    )


def parse_llm_json(text: str) -> dict[str, Any]:
    stripped = text.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", stripped)
    if fence:
        stripped = fence.group(1).strip()
    return json.loads(stripped)


def default_completer(config: RagConfig) -> Completer:
    from llama_index.llms.ollama import Ollama

    llm = Ollama(
        model=config.ollama_model,
        base_url=config.ollama_base_url,
        request_timeout=float(config.ollama_request_timeout),
    )

    def complete(prompt: str) -> str:
        response = llm.complete(prompt)
        return str(response)

    return complete


class RootCauseAgent:
    """Reads an alarm payload, retrieves KB sections, returns grounded causes."""

    def __init__(
        self,
        config: RagConfig,
        *,
        completer: Completer | None = None,
    ) -> None:
        self.config = config
        self._completer = completer

    def _get_completer(self) -> Completer:
        if self._completer is not None:
            return self._completer
        return default_completer(self.config)

    def propose(
        self,
        payload: AlarmPayload | str,
        *,
        top_k: int | None = None,
        use_retrieval: bool = True,
    ) -> AgentAnswer:
        if isinstance(payload, str):
            alarm = AlarmPayload(
                turbine_id="unknown",
                alarm_code=payload.strip(),
                timestamp="",
                snapshot={},
            )
        else:
            alarm = payload
        alarm_text = format_alarm_text(alarm)

        hits: list[Hit] = []
        if use_retrieval:
            query = formulate_query(alarm)
            hits = retrieve(query, self.config, top_k=top_k)
            if not hits:
                return abstain_answer()

        prompt = build_prompt(alarm_text, hits, use_retrieval=use_retrieval)
        raw = self._get_completer()(prompt)
        try:
            data = parse_llm_json(raw)
        except json.JSONDecodeError:
            return abstain_answer()

        raw_causes = data.get("causes") or []
        if not isinstance(raw_causes, list):
            return abstain_answer()

        cause_dicts: list[dict[str, str]] = []
        for item in raw_causes:
            if isinstance(item, dict):
                cause_dicts.append({k: str(v) for k, v in item.items()})

        if not use_retrieval:
            if not cause_dicts:
                return abstain_answer(
                    next_check=str(data.get("next_check", "")),
                    confidence=str(data.get("confidence", "low")),
                )
            return AgentAnswer(
                status="baseline",
                causes=tuple(),
                next_check=str(data.get("next_check", "")),
                confidence=str(data.get("confidence", "")),
                message=json.dumps({"causes": cause_dicts}),
            )

        return build_agent_answer(
            cause_dicts,
            hits,
            next_check=str(data.get("next_check", "")),
            confidence=str(data.get("confidence", "")),
        )


def format_answer(answer: AgentAnswer) -> str:
    if answer.is_abstain:
        return NO_GROUNDED_CAUSE
    lines: list[str] = []
    for i, c in enumerate(answer.causes, start=1):
        lines.append(f"{i}. {c.cause}")
        lines.append(f"   source: {c.source}")
        lines.append(f'   quote: "{c.quote}"')
        lines.append(f"   SCADA: {c.supporting_signal}")
    lines.append(f"Next check: {answer.next_check}")
    lines.append(f"Confidence: {answer.confidence}")
    return "\n".join(lines)
