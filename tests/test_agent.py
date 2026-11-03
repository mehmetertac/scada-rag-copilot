"""Agent loop with injectable completer."""

from __future__ import annotations

import json

from scada_rag.agent import RootCauseAgent, build_prompt
from scada_rag.alarms import AlarmPayload
from scada_rag.config import RagConfig
from scada_rag.grounding import NO_GROUNDED_CAUSE
from scada_rag.ingest import ingest
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
    assert "gearbox_hss_bearing_overtemp.md" in prompt
    assert "Do not invent OEM trip setpoints" in prompt


def test_propose_abstains_when_citations_invalid(tmp_path, fixture_kb) -> None:
    config = RagConfig.load(embed_mode="mock", persist_dir=tmp_path / "chroma", kb_dir=fixture_kb)
    ingest(config)
    agent = RootCauseAgent(
        config,
        completer=lambda p: json.dumps(
            {
                "causes": [
                    {
                        "cause": "Invented",
                        "source": "gearbox.md",
                        "quote": "this exact phrase is not in the chunk",
                        "supporting_signal": "x",
                    }
                ],
                "next_check": "n/a",
                "confidence": "low",
            }
        ),
    )
    payload = AlarmPayload(
        turbine_id="T",
        alarm_code="gearbox HSS bearing",
        timestamp="t",
        snapshot={"Gear_Bear_Temp_Avg": 70},
    )
    answer = agent.propose(payload)
    assert answer.is_abstain
    assert NO_GROUNDED_CAUSE in answer.message


def test_propose_grounded_with_fake_completer(tmp_path, fixture_kb) -> None:
    from scada_rag.alarms import formulate_query
    from scada_rag.retrieve import retrieve

    config = RagConfig.load(embed_mode="mock", persist_dir=tmp_path / "chroma", kb_dir=fixture_kb)
    ingest(config)
    payload = AlarmPayload(
        turbine_id="T06",
        alarm_code="gearbox HSS bearing temperature",
        timestamp="t",
        snapshot={"Gear_Bear_Temp_Avg": 70},
    )
    hits = retrieve(formulate_query(payload), config, top_k=10)
    hit = hits[0]
    quote = hit.text.split("\n")[-1][:40].strip() or "bearing"

    def completer(prompt: str) -> str:
        return json.dumps(
            {
                "causes": [
                    {
                        "cause": "HSS bearing or lubrication at partial load",
                        "source": hit.source,
                        "quote": quote,
                        "supporting_signal": "Gear_Bear_Temp_Avg",
                    }
                ],
                "next_check": "Plot 7 days bearing vs oil",
                "confidence": "medium",
            }
        )

    agent = RootCauseAgent(config, completer=completer)
    answer = agent.propose(payload)
    assert not answer.is_abstain
    assert len(answer.causes) == 1
    assert answer.causes[0].source == "gearbox.md"
    assert answer.causes[0].quote == quote
