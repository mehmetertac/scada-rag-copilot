# AGENT.md — rules for AI agents

Guidance for agents working in **scada-rag-copilot**. Read this file first, then follow the linked docs.

---

## Documentation map

| Doc | Purpose |
| --- | --- |
| [README.md](README.md) | Setup, grounded agent, eval table, limitations |
| [handover.md](handover.md) | Status, layout, module API, next step |
| [CHANGELOG.md](CHANGELOG.md) | Unreleased day-1 notes |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Retrieval flow, chunk metadata, twin boundary |
| [configs/rag.yaml](configs/rag.yaml) | Embed model, chunk size, Chroma path, Ollama model name |
| [kb/](kb/) | Fault-mode notes, inspection checklist, escalation, EDP tag glossary |
| [src/scada_rag/](src/scada_rag/) | `kb_loader`, `ingest`, `retrieve`, `agent`, `sanity` |
| [tests/](tests/) | Unit tests (mock embeddings), CLI smoke, real-model sanity queries |
| [eval/alarms.yaml](eval/alarms.yaml) | Labelled synthetic alarms for eval |
| [notebooks/01_demo.ipynb](notebooks/01_demo.ipynb) | Ingest, sanity queries, one grounded alarm |
| [results/sanity_queries.md](results/sanity_queries.md) | Last top-3 table for the five queries |
| [wind-digital-twin](https://github.com/mehmetertac/wind-digital-twin) | Gearbox thermal twin. Cite residuals; do not import it |
| [wind-turbine-anomaly](https://github.com/mehmetertac/wind-turbine-anomaly) | Earlier physics-residual baseline |
| [grid-gnn-faults](https://github.com/mehmetertac/grid-gnn-faults) | Grid-fault classifier for electrical alarms |

Headline contract: every ranked cause must cite a retrieved chunk or the agent abstains; the twin/GNN fields on the payload are context only; no invented setpoints or fake twin queries.

---

## Rules

### 1. File size limit

- **No file should exceed 1,000 lines.**
- If a file approaches or exceeds that limit, **stop and suggest a refactor** before adding more code.
- Pre-commit runs [`scripts/check_file_size.py`](scripts/check_file_size.py).

### 2. Documentation before every push

- **Update documentation before every push** to the repository.
- At minimum, check [README.md](README.md), [handover.md](handover.md), and [CHANGELOG.md](CHANGELOG.md).
- If retrieval behavior or the knowledge base changes, update [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) or the affected `kb/` note.

### 2a. Update handover.md on every push (required)

- Refresh **Last updated**, **What is done**, **Repo layout**, **Core module API**, **Suggested next step**, and **Key commit** on each push.
- If nothing functional changed, still bump **Last updated** and note "no functional change."

### 3. Tests — always, at least minimal

- **Always create at least minimal unit tests**, even for small changes.
- Add **integration** tests when wiring ingest and retrieve (real `bge-small` against `kb/`).
- Add **functional** tests for the CLIs (`python -m scada_rag.ingest`, `python -m scada_rag.retrieve`).
- Unit tests use `--embed-mode mock` and a temporary Chroma directory. They must not download a model.

### 4. Run tests before commit or push

```powershell
pytest tests/ -q
python scripts/check_file_size.py
```

**Git hooks:** After creating the venv:

```powershell
pip install -e ".[dev]"
pre-commit install
```

Hooks run the file-size check and pytest (see [`.pre-commit-config.yaml`](.pre-commit-config.yaml)). If hooks do not exist yet, create them.

### 5. Keep reading in-repo docs

- Do not guess the pipeline or the day-2 boundary from memory. Use [handover.md](handover.md) and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).
- Do not invent OEM trip setpoints in `kb/`. Label site-practice numbers as examples and point at the alarm manual.

---

## Quick checklist (before push)

- [ ] No file > 1,000 lines (or a refactor proposed)
- [ ] [README.md](README.md) updated if behavior or layout changed
- [ ] [handover.md](handover.md) updated (required on every push)
- [ ] [CHANGELOG.md](CHANGELOG.md) updated
- [ ] New or changed logic has tests in [tests/](tests/)
- [ ] `pytest tests/ -q` passes
- [ ] `python scripts/check_file_size.py` passes
