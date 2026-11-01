# scada-rag-copilot

A local retrieval copilot for wind-turbine SCADA alarms. You pass alarm text. It returns the knowledge-base sections most likely to explain it: gearbox HSS bearing versus oil cooler, a blade-2 pitch deviation, a generator NDE bearing trend, and when a temperature alarm is a stop.

Day 1 is the knowledge base and retrieval. `RootCauseAgent.propose` is the day-2 chat step (Ollama, `qwen2.5:3b`). It raises `NotImplementedError` until that model is installed. The hybrid twin in [wind-digital-twin](https://github.com/mehmetertac/wind-digital-twin) is evidence the notes tell you to request. This repository does not call it.

Pipeline and the twin boundary: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). Status and module API: [handover.md](handover.md). Agent rules: [AGENT.md](AGENT.md).

## Quickstart

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pre-commit install

python -m scada_rag.ingest
python -m scada_rag.retrieve --query "gearbox HSS bearing temp rising at partial load"
pytest tests/ -q
python scripts/sanity_queries.py
```

`scripts/sanity_queries.py` rebuilds the index and writes [results/sanity_queries.md](results/sanity_queries.md). The first ingest downloads `BAAI/bge-small-en-v1.5` (about 130 MB) and writes `storage/chroma/`, which is gitignored. Ingest and retrieve do not need an API key and do not need Ollama.

## Sanity check

Five queries must return the expected note in the top 3. Latest run: [results/sanity_queries.md](results/sanity_queries.md).

| Query | Expected note |
| --- | --- |
| gearbox HSS bearing temp rising at partial load | `gearbox_hss_bearing_overtemp.md` |
| gearbox oil temperature high but bearing normal | `gearbox_oil_overtemp.md` |
| pitch angle deviation alarm blade 2 | `pitch_system_errors.md` |
| generator NDE bearing temperature trend | `generator_bearing_faults.md` |
| when to stop the turbine for a gearbox temperature alarm | `procedure_escalation_thresholds.md` |

## Layout

| Path | Role |
| --- | --- |
| [kb/](kb/) | 13 short notes: fault modes, drivetrain inspection, escalation, EDP tag glossary |
| [src/scada_rag/ingest.py](src/scada_rag/ingest.py) | Split on `##`, chunk (~400 tokens, 60 overlap), embed, persist |
| [src/scada_rag/retrieve.py](src/scada_rag/retrieve.py) | Top-k hits with title, section, source |
| [src/scada_rag/agent.py](src/scada_rag/agent.py) | Prompt builder and the unimplemented chat call |
| [configs/rag.yaml](configs/rag.yaml) | Model, chunking, store path |
| [notebooks/01_demo.ipynb](notebooks/01_demo.ipynb) | Same ingest and five queries |

Settings live in [configs/rag.yaml](configs/rag.yaml). `embed_mode: mock` is a hash embedder for tests, not for the demo.

## Day 2

Install [Ollama](https://ollama.com), then `ollama pull qwen2.5:3b`. The model name is already `ollama_model` in the config. Until `propose` is implemented, use `retrieve()` and `build_prompt()`.

## Limits

- Notes are field judgment for a portfolio copilot, not an OEM alarm manual. Where a number appears, the note says to confirm the platform setpoint.
- No live SCADA connection. No start, stop, or reset commands.
- Tag names follow the public EDP layout (`Gear_Bear_Temp_Avg`, `Gear_Oil_Temp_Avg`, `Gen_Bear_Temp_Avg`, `Hyd_Oil_Temp_Avg`, and the others in [kb/glossary_edp_scada_tags.md](kb/glossary_edp_scada_tags.md)). Confirm them on the site signal list.
