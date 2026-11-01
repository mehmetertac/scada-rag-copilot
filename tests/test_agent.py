"""Day-2 agent surface: prompt builder works, chat completion does not."""

from __future__ import annotations

import pytest

from scada_rag.agent import RootCauseAgent, build_prompt
from scada_rag.config import RagConfig
from scada_rag.retrieve import Hit


def test_build_prompt_includes_alarm_and_source() -> None:
    hit = Hit(
        score=0.5,
        doc_title="Gearbox HSS bearing over-temperature",
        section="Symptoms in SCADA",
        source="gearbox_hss_bearing_overtemp.md",
        text="Bearing rises at partial load.",
        component="gearbox",
        doc_type="fault",
    )
    prompt = build_prompt("HSS bearing temp rising", [hit])
    assert "HSS bearing temp rising" in prompt
    assert "Gearbox HSS bearing over-temperature" in prompt
    assert "gearbox_hss_bearing_overtemp.md" in prompt
    assert "Do not invent OEM trip setpoints" in prompt


def test_propose_is_not_implemented(tmp_path) -> None:
    config = RagConfig.load(embed_mode="mock", persist_dir=tmp_path / "chroma", kb_dir=tmp_path)
    agent = RootCauseAgent(config)
    with pytest.raises(NotImplementedError, match="ollama pull"):
        agent.propose("gearbox oil temperature high")
