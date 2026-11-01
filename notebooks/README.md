# Notebooks

Notebooks are thin drivers. Ingest, retrieval, and the sanity queries live in `src/scada_rag/`.

| Notebook | What it does |
| --- | --- |
| [01_demo.ipynb](01_demo.ipynb) | Ingest `kb/` with the config in `configs/rag.yaml`, then run the five sanity queries |

Run it from the repository root with the project venv so `bge-small` and Chroma match the CLI. The first run downloads the embedding model.
