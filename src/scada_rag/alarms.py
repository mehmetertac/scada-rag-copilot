"""Simulated alarm payloads and retrieval query formulation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ShapSensor:
    tag: str
    contribution: float


@dataclass(frozen=True)
class AlarmPayload:
    turbine_id: str
    alarm_code: str
    timestamp: str
    snapshot: dict[str, float | int | str]
    anomaly_score: float | None = None
    shap_sensors: tuple[ShapSensor, ...] = field(default_factory=tuple)

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> AlarmPayload:
        shap_raw = data.get("shap_sensors") or []
        shap = tuple(
            ShapSensor(tag=str(item["tag"]), contribution=float(item["contribution"]))
            for item in shap_raw
        )
        score = data.get("anomaly_score")
        return cls(
            turbine_id=str(data["turbine_id"]),
            alarm_code=str(data["alarm_code"]),
            timestamp=str(data["timestamp"]),
            snapshot=dict(data.get("snapshot") or {}),
            anomaly_score=float(score) if score is not None else None,
            shap_sensors=shap,
        )


def format_alarm_text(payload: AlarmPayload) -> str:
    lines = [
        f"turbine_id: {payload.turbine_id}",
        f"alarm_code: {payload.alarm_code}",
        f"timestamp: {payload.timestamp}",
        "SCADA snapshot:",
    ]
    for tag, value in sorted(payload.snapshot.items()):
        lines.append(f"  {tag}: {value}")
    if payload.anomaly_score is not None:
        lines.append(f"anomaly_score: {payload.anomaly_score}")
    if payload.shap_sensors:
        lines.append("top SHAP sensors (from grid-gnn-faults / twin context, not queried here):")
        for s in payload.shap_sensors:
            lines.append(f"  {s.tag}: {s.contribution:.4f}")
    return "\n".join(lines)


def formulate_query(payload: AlarmPayload) -> str:
    """Build a retrieval query from alarm code, tags, and optional SHAP names."""
    parts = [payload.alarm_code]
    parts.extend(sorted(payload.snapshot.keys()))
    for s in payload.shap_sensors:
        parts.append(s.tag)
    return " ".join(parts)
