"""Citation gate and eval scoring helpers."""

from __future__ import annotations

from scada_rag.eval_alarms import hit_top1, hit_top3, grounding_check, summarize_rag
from scada_rag.eval_alarms import ScenarioScores
from scada_rag.grounding import (
    AgentAnswer,
    GroundedCause,
    build_agent_answer,
    filter_grounded_causes,
    quote_in_hit,
)
from scada_rag.retrieve import Hit


def _hit(source: str, text: str) -> Hit:
    return Hit(
        score=0.9,
        doc_title="T",
        section="Likely causes",
        source=source,
        text=text,
        component="gearbox",
        doc_type="fault",
    )


def test_quote_in_hit_substring() -> None:
    hit = _hit("gearbox_hss_bearing_overtemp.md", "Bearing rises at partial load.")
    assert quote_in_hit("partial load", hit)
    assert not quote_in_hit("invented text", hit)


def test_filter_grounded_causes_drops_bad_source_and_quote() -> None:
    hits = [_hit("gearbox_hss_bearing_overtemp.md", "HSS bearing damage at partial load.")]
    raw = [
        {
            "cause": "HSS bearing damage",
            "source": "gearbox_hss_bearing_overtemp.md",
            "quote": "HSS bearing damage at partial load",
            "supporting_signal": "Gear_Bear_Temp_Avg",
        },
        {
            "cause": "Fake",
            "source": "not_in_retrieval.md",
            "quote": "anything",
            "supporting_signal": "x",
        },
    ]
    kept = filter_grounded_causes(raw, hits)
    assert len(kept) == 1
    assert kept[0].source == "gearbox_hss_bearing_overtemp.md"


def test_build_agent_answer_abstains_when_nothing_passes() -> None:
    ans = build_agent_answer([], [_hit("a.md", "body")], next_check="look", confidence="low")
    assert ans.is_abstain


def test_hit_top1_and_top3() -> None:
    cause = GroundedCause("c", "gearbox_oil_overtemp.md", "q", "Gear_Oil_Temp_Avg")
    ans = AgentAnswer(status="grounded", causes=(cause,), next_check="", confidence="high")
    assert hit_top1(ans, "gearbox_oil_overtemp.md")
    assert hit_top3(ans, "gearbox_oil_overtemp.md")
    assert not hit_top1(ans, "abstain")


def test_summarize_rag() -> None:
    rows = [
        ScenarioScores("a", "x.md", True, True, True, ["x.md"]),
        ScenarioScores("b", "y.md", False, True, True, ["z.md", "y.md"]),
    ]
    s = summarize_rag(rows)
    assert s["top1"] == 0.5
    assert s["top3"] == 1.0
