# Changelog

## [0.1.0] - 2026-11-03

### Added

- `AlarmPayload` and deterministic retrieval query formulation from alarm + SCADA tags + optional SHAP context.
- `RootCauseAgent.propose`: retrieve → Ollama JSON → citation gate; abstains with **no grounded cause found** when citations fail.
- `grounding.py` citation gate (source must match a retrieved chunk; quote must be a verbatim substring).
- Twelve labelled synthetic alarms in `eval/alarms.yaml` and `python -m scada_rag.eval_alarms` (RAG vs no-retrieval baseline).
- Demo notebook: sanity queries + one grounded alarm.
- Tests for alarms, grounding, agent (injectable completer), and eval YAML load.

### Unchanged from day 1

- Local wind-turbine knowledge base, `bge-small` ingest, Chroma store, five-query sanity check.

[0.1.0]: https://github.com/mehmetertac/scada-rag-copilot/releases/tag/v0.1.0
