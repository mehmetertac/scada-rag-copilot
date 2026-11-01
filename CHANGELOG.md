# Changelog

## [Unreleased]

### Added

- Local wind-turbine knowledge base: gearbox, generator, pitch, converter, yaw, hydraulic, and grid notes, plus an inspection checklist, escalation procedure, and EDP SCADA tag glossary.
- Ingest path that splits notes on headings, chunks them, and embeds them with `BAAI/bge-small-en-v1.5` into a persistent Chroma store.
- Top-k retrieval with document title, section, and source file.
- Day-2 agent stub. `build_prompt` is usable; `RootCauseAgent.propose` waits on a local Ollama model.
- Five-query sanity check and tests (mock embedder, CLI, real-model retrieval).
