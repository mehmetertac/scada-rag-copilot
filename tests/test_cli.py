"""CLI smoke: ingest a fixture store, then retrieve from it."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from scada_rag.config import repo_root


def test_retrieve_cli_exits_zero(tmp_path: Path, fixture_kb: Path) -> None:
    persist = tmp_path / "chroma"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root() / "src")
    env["ANONYMIZED_TELEMETRY"] = "False"
    common = [
        sys.executable,
        "-m",
        "scada_rag.ingest",
        "--embed-mode",
        "mock",
        "--kb-dir",
        str(fixture_kb),
        "--persist-dir",
        str(persist),
    ]
    subprocess.run(common, check=True, cwd=repo_root(), env=env)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "scada_rag.retrieve",
            "--query",
            "bearing temperature",
            "--embed-mode",
            "mock",
            "--persist-dir",
            str(persist),
            "--top-k",
            "2",
        ],
        check=True,
        cwd=repo_root(),
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "score=" in result.stdout
    assert "[" in result.stdout and ".md]" in result.stdout
