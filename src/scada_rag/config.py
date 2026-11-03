"""Load ``configs/rag.yaml`` into a typed config."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

_PATH_FIELDS = ("persist_dir", "kb_dir")


def repo_root() -> Path:
    """Repository root (parent of ``src``)."""
    return Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class RagConfig:
    embed_model: str
    embed_mode: str
    chunk_size: int
    chunk_overlap: int
    top_k: int
    collection: str
    persist_dir: Path
    kb_dir: Path
    ollama_model: str
    ollama_base_url: str
    ollama_request_timeout: float

    @classmethod
    def load(cls, path: Path | None = None, **overrides: Any) -> RagConfig:
        root = repo_root()
        config_path = path or (root / "configs" / "rag.yaml")
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        if not isinstance(raw, dict):
            raise ValueError(f"{config_path} must be a mapping")

        data: dict[str, Any] = dict(raw)
        for key, value in overrides.items():
            if value is not None:
                data[key] = value

        if str(data.get("embed_model", "")).strip().lower() == "mock":
            data["embed_mode"] = "mock"

        for key in _PATH_FIELDS:
            resolved = Path(data[key])
            if not resolved.is_absolute():
                resolved = root / resolved
            data[key] = resolved

        known = {field for field in cls.__dataclass_fields__}
        extra = set(data) - known
        if extra:
            raise ValueError(f"Unknown config keys: {sorted(extra)}")
        return cls(**data)
