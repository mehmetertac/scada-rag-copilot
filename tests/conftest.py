"""Shared fixtures. The real embedding model is not loaded here."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def fixture_kb(tmp_path: Path) -> Path:
    kb = tmp_path / "kb"
    kb.mkdir()
    (kb / "gearbox.md").write_text(
        """---
title: Gearbox HSS bearing over-temperature
component: gearbox
doc_type: fault
tags: [bearing, hss]
---

# Gearbox HSS bearing over-temperature

High-speed shaft bearing temperature at partial load.

## Symptoms in SCADA

Gear_Bear_Temp_Avg rises at partial load while Gear_Oil_Temp_Avg stays flat.

## Likely causes

Bearing damage or lubrication starvation at the HSS bearing.
""",
        encoding="utf-8",
    )
    (kb / "pitch.md").write_text(
        """---
title: Pitch system errors
component: pitch
doc_type: fault
tags: [pitch, blade]
---

# Pitch system errors

Blade pitch disagreement.

## Symptoms in SCADA

Pitch angle deviation alarm on blade 2 with Blds_PitchAngle_Std high.
""",
        encoding="utf-8",
    )
    (kb / "plain.md").write_text(
        """# Notes without front matter

A short overview.

## Empty heading below is skipped

Body of the only real section.
""",
        encoding="utf-8",
    )
    return kb
