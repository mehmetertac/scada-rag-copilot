"""Evaluate grounded agent vs no-retrieval baseline on labelled alarm scenarios."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from scada_rag.agent import RootCauseAgent, default_completer
from scada_rag.alarms import AlarmPayload
from scada_rag.config import RagConfig, repo_root
from scada_rag.grounding import AgentAnswer, NO_GROUNDED_CAUSE


@dataclass(frozen=True)
class Scenario:
    id: str
    expected_source: str
    payload: AlarmPayload


@dataclass
class ScenarioScores:
    scenario_id: str
    expected_source: str
    top1: bool
    top3: bool
    grounding_ok: bool
    cited_sources: list[str]


@dataclass
class BaselineScores:
    scenario_id: str
    hallucinated_manual: bool
    names_labelled_note: bool


def load_scenarios(path: Path | None = None) -> list[Scenario]:
    root = repo_root()
    yaml_path = path or (root / "eval" / "alarms.yaml")
    raw = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    out: list[Scenario] = []
    for item in raw.get("scenarios") or []:
        payload = AlarmPayload.from_mapping(item)
        out.append(
            Scenario(
                id=str(item["id"]),
                expected_source=str(item["expected_source"]),
                payload=payload,
            )
        )
    return out


def hit_top1(answer: AgentAnswer, expected: str) -> bool:
    if expected == "abstain":
        return answer.is_abstain
    if answer.is_abstain or not answer.causes:
        return False
    return answer.causes[0].source == expected


def hit_top3(answer: AgentAnswer, expected: str) -> bool:
    if expected == "abstain":
        return answer.is_abstain
    if answer.is_abstain:
        return False
    sources = [c.source for c in answer.causes[:3]]
    return expected in sources


def grounding_check(answer: AgentAnswer, expected: str) -> bool:
    """All citations passed the runtime gate; relevance = top cause cites expected when grounded."""
    if answer.is_abstain:
        return expected == "abstain"
    if not answer.causes:
        return False
    for c in answer.causes:
        if not c.source.endswith(".md"):
            return False
    if expected == "abstain":
        return False
    return any(c.source == expected for c in answer.causes)


def score_rag(agent: RootCauseAgent, scenarios: list[Scenario]) -> list[ScenarioScores]:
    rows: list[ScenarioScores] = []
    for i, sc in enumerate(scenarios, start=1):
        print(f"RAG {i}/{len(scenarios)}: {sc.id}", flush=True)
        answer = agent.propose(sc.payload, use_retrieval=True)
        rows.append(
            ScenarioScores(
                scenario_id=sc.id,
                expected_source=sc.expected_source,
                top1=hit_top1(answer, sc.expected_source),
                top3=hit_top3(answer, sc.expected_source),
                grounding_ok=grounding_check(answer, sc.expected_source),
                cited_sources=[c.source for c in answer.causes],
            )
        )
    return rows


def baseline_hallucinated_manual(text: str) -> bool:
    return bool(re.search(r"\b[a-z0-9_]+\.md\b", text, re.I))


def baseline_names_note(text: str, expected: str) -> bool:
    if expected == "abstain":
        return False
    stem = expected.replace(".md", "").replace("_", " ")
    return expected in text or stem.split()[0] in text.lower()


def score_baseline(agent: RootCauseAgent, scenarios: list[Scenario]) -> list[BaselineScores]:
    rows: list[BaselineScores] = []
    for i, sc in enumerate(scenarios, start=1):
        print(f"Baseline {i}/{len(scenarios)}: {sc.id}", flush=True)
        answer = agent.propose(sc.payload, use_retrieval=False)
        blob = answer.message or answer.next_check
        if answer.status == "baseline":
            blob = answer.message
        rows.append(
            BaselineScores(
                scenario_id=sc.id,
                hallucinated_manual=baseline_hallucinated_manual(blob),
                names_labelled_note=baseline_names_note(blob, sc.expected_source),
            )
        )
    return rows


def summarize_rag(rows: list[ScenarioScores]) -> dict[str, float]:
    n = len(rows) or 1
    return {
        "top1": sum(1 for r in rows if r.top1) / n,
        "top3": sum(1 for r in rows if r.top3) / n,
        "grounding": sum(1 for r in rows if r.grounding_ok) / n,
    }


def summarize_baseline(rows: list[BaselineScores]) -> dict[str, float]:
    n = len(rows) or 1
    return {
        "hallucinated_manual": sum(1 for r in rows if r.hallucinated_manual) / n,
        "names_labelled_note": sum(1 for r in rows if r.names_labelled_note) / n,
    }


def render_markdown(
    rag_rows: list[ScenarioScores],
    rag_summary: dict[str, float],
    base_rows: list[BaselineScores],
    base_summary: dict[str, float],
    *,
    model: str,
) -> str:
    lines = [
        "# Alarm eval (grounded RAG vs no-retrieval baseline)",
        "",
        f"Model: `{model}`. Scenarios: {len(rag_rows)} from `eval/alarms.yaml`.",
        "",
        "## Summary",
        "",
        "| Metric | RAG | No retrieval |",
        "| --- | --- | --- |",
        f"| Top-1 cause hit rate | {rag_summary['top1']:.0%} | — |",
        f"| Top-3 cause hit rate | {rag_summary['top3']:.0%} | — |",
        f"| Grounding check pass rate | {rag_summary['grounding']:.0%} | — |",
        f"| Answers citing a `.md` manual section | — | {base_summary['hallucinated_manual']:.0%} |",
        f"| Answers naming labelled note (specificity) | — | {base_summary['names_labelled_note']:.0%} |",
        "",
        "## Per scenario (RAG)",
        "",
        "| id | expected | top-1 | top-3 | grounding | cited |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for r in rag_rows:
        lines.append(
            f"| {r.scenario_id} | {r.expected_source} | "
            f"{'yes' if r.top1 else 'no'} | {'yes' if r.top3 else 'no'} | "
            f"{'yes' if r.grounding_ok else 'no'} | {', '.join(r.cited_sources) or NO_GROUNDED_CAUSE} |"
        )
    lines.extend(["", "## Per scenario (baseline)", "", "| id | hallucinated .md | names note |", "| --- | --- | --- |"])
    for b in base_rows:
        lines.append(
            f"| {b.scenario_id} | {'yes' if b.hallucinated_manual else 'no'} | "
            f"{'yes' if b.names_labelled_note else 'no'} |"
        )
    lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run alarm eval and write results/eval_alarms.md")
    p.add_argument("--config", type=Path, default=None)
    p.add_argument("--eval-file", type=Path, default=None)
    p.add_argument("--output", type=Path, default=None)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = RagConfig.load(path=args.config)
    scenarios = load_scenarios(args.eval_file)
    agent = RootCauseAgent(config, completer=default_completer(config))
    rag_rows = score_rag(agent, scenarios)
    base_rows = score_baseline(agent, scenarios)
    md = render_markdown(
        rag_rows,
        summarize_rag(rag_rows),
        base_rows,
        summarize_baseline(base_rows),
        model=config.ollama_model,
    )
    out = args.output or (repo_root() / "results" / "eval_alarms.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
