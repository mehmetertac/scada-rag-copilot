"""Load eval scenarios from YAML."""

from __future__ import annotations

from pathlib import Path

from scada_rag.config import repo_root
from scada_rag.eval_alarms import load_scenarios


def test_load_scenarios_count() -> None:
    path = repo_root() / "eval" / "alarms.yaml"
    scenarios = load_scenarios(path)
    assert len(scenarios) == 12
    abstain = [s for s in scenarios if s.expected_source == "abstain"]
    assert len(abstain) == 1
