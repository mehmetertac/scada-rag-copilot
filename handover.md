# handover.md

**Last updated:** 2026-11-01

Day 1 of the SCADA alarm root-cause copilot: a local knowledge base and top-k retrieval. Chat completion is not wired. The hybrid twin is referenced from the notes and is not a Python dependency.

---

## What is done

| Item | Status |
| --- | --- |
| Go / no-go on wind-digital-twin `v1.0.0` (README tables, Streamlit figure) | Passed; this repo proceeded |
| Variant | SCADA alarm root-cause agent, not the IEEE/CIGRE PDF ingest |
| Stack | llama-index, `BAAI/bge-small-en-v1.5` on CPU, Chroma. Ollama `qwen2.5:3b` named for day 2 |
| `kb/` — 13 markdown notes with front matter | Done |
| `ingest` / `retrieve` CLIs, persistent store under `storage/chroma/` (gitignored) | Done |
| Five sanity queries, expected source in the top 3 | See [results/sanity_queries.md](results/sanity_queries.md) |
| `RootCauseAgent.propose` | Stub. Raises `NotImplementedError` |
| Tests and pre-commit (file size + pytest) | Done |
| Git remote `origin` → [scada-rag-copilot](https://github.com/mehmetertac/scada-rag-copilot) | This push |

---

## Repo layout

```
kb/                 fault notes, checklist, escalation, tag glossary
src/scada_rag/      config, kb_loader, embeddings, store, ingest, retrieve, agent, sanity
configs/rag.yaml    model, chunk size, paths, Ollama model name
scripts/            file-size check, sanity-query report
tests/              mock unit tests, CLI, real-model integration
notebooks/          01_demo.ipynb
docs/ARCHITECTURE.md
results/sanity_queries.md
```

---

## Core module API

| Symbol | Role |
| --- | --- |
| `RagConfig.load` | Read `configs/rag.yaml`. Overrides: `embed_mode`, `persist_dir`, `kb_dir` |
| `load_kb(kb_dir)` | Front matter + `##` sections → llama-index documents with metadata |
| `ingest(config)` | Rebuild the Chroma collection. Returns the chunk count |
| `retrieve(query, config, top_k=None)` | List of `Hit` (`score`, `doc_title`, `section`, `source`, `text`) |
| `build_prompt(alarm_text, hits)` | Day-2 prompt. Evidence is the retrieved text only |
| `RootCauseAgent.propose` | Not implemented. Needs `ollama pull qwen2.5:3b` |

CLIs: `python -m scada_rag.ingest`, `python -m scada_rag.retrieve --query "..."`.

---

## Suggested next step

1. Install Ollama and `ollama pull qwen2.5:3b`.
2. Implement `RootCauseAgent.propose` with `llama-index-llms-ollama`, calling `retrieve` then `build_prompt`.
3. Add a fixture alarm transcript and a test that the answer cites a retrieved file name. Do not assert a specific root cause as ground truth.

---

## Key commit

Day-1 retrieval commit on `main`. Hash recorded in the push that added this file; if you are reading it in that commit, `git log -1` is the hash.
