# Notebooks

Notebooks are thin drivers. Ingest, retrieval, and the sanity queries live in `src/scada_rag/`.

| Notebook | What it does |
| --- | --- |
| [01_demo.ipynb](01_demo.ipynb) | Ingest, five sanity queries, one alarm through `RootCauseAgent.propose` |

Run from the repository root with the project venv. Needs Ollama and `qwen2.5:3b` for the agent cell. The first ingest downloads the embedding model.
