# handover.md

**Last updated:** 2026-11-03

v0.1.0: grounded alarm agent, eval set, demo notebook. LLM sub-track complete — do not extend agent tools beyond retrieval on the next session.

---

## What is done

| Item | Status |
| --- | --- |
| Local KB (13 notes), ingest, retrieve, sanity queries | Done |
| `AlarmPayload`, `formulate_query`, citation gate | Done |
| `RootCauseAgent.propose` via Ollama `qwen2.5:3b` + JSON | Done |
| `eval/alarms.yaml` (12 scenarios), `python -m scada_rag.eval_alarms` | Done |
| Demo [notebooks/01_demo.ipynb](notebooks/01_demo.ipynb) | Done |
| Tests (mock embedder + fake completer) | Done |
| Git remote `origin` → [scada-rag-copilot](https://github.com/mehmetertac/scada-rag-copilot) | Tag `v0.1.0` on push |

---

## Repo layout

```
kb/                 fault notes, checklist, escalation, tag glossary
eval/alarms.yaml    labelled synthetic alarms
src/scada_rag/      config, kb_loader, embeddings, store, ingest, retrieve,
                    alarms, grounding, agent, eval_alarms, sanity
configs/rag.yaml
scripts/            file-size check, sanity-query report
tests/
notebooks/          01_demo.ipynb
docs/ARCHITECTURE.md
results/sanity_queries.md, results/eval_alarms.md
```

---

## Core module API

| Symbol | Role |
| --- | --- |
| `RagConfig.load` | Read `configs/rag.yaml` |
| `ingest` / `retrieve` | Build Chroma index, top-k `Hit` list |
| `AlarmPayload`, `formulate_query`, `format_alarm_text` | Simulated alarm → retrieval query |
| `RootCauseAgent.propose(payload, use_retrieval=True)` | Returns `AgentAnswer` (grounded or abstain) |
| `build_prompt`, `format_answer` | Prompt text and human-readable output |
| `load_scenarios`, `main` in `eval_alarms` | Eval CLI |

CLIs: `python -m scada_rag.ingest`, `python -m scada_rag.retrieve --query "..."`, `python -m scada_rag.eval_alarms`.

---

## Suggested next step

**Outside this sub-track:** portfolio integration (live alarm webhook), larger KB, or twin `/twin/rul` as an agent tool — not scheduled for the LLM/RAG track closure.

---

## Key commit

*(fill after push)* — v0.1.0 grounded agent and eval.
