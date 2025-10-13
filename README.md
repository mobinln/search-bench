# Search Systems Benchmark

A comprehensive comparison of different search approaches for product search,
with real benchmarks and interactive demos.

## 🎯 Goal

When building an application that needs search, which system should you use?
This project benchmarks and compares multiple different approaches across latency,
relevance, features, and operational complexity.

## Methodology

We have a `data_generator.py` script which generate multiple sample data for us and also in this file we have a list of sample queries which we use to benchmark our engines, We have a `search_engine.py` file which includes our abstraction around `SearchEngine` to unify our integrations with different engines so we don't need to change our benchmark or data, We just replace the engine and everything works and also our implementations are clean and readable, Our benchmark is mostly async single thread because we want to test how different approaches react in a single-machine, Also the benchmark below ran on a Macbook M1 Pro machine

## 🔍 Systems Compared

- SQLite FTS5
- PostgreSQL Full-Text Search
- PostgreSQL with pg_trgm (trigrams)
- Redis with Redis Search
- Meilisearch
- Apache Solr
- Typesense
- SurrealDB

## 📊 Key Findings

- **Fastest**: TBD
- **Best relevance**: TBD
- **Easiest setup**: Sqlite FTS5
- **Lowest resource usage**: Sqlite FTS5
- **Best for <10k docs**: Redis Search
- **Best for <100k docs**: Redis Search
- **Best for >1M docs**: TBD

| Engine        | Latency (10k) | Latency (100k) | RAM (100k) | Typo Tolerance | Ease of setup and use                                                                        |
| ------------- | ------------- | -------------- | ---------- | -------------- | -------------------------------------------------------------------------------------------- |
| Sqlite FTS5   | ~1.8 ms       | ~0.8 ms        | ~150 MB    | No             | 4/5 (You should create a VIRTUAL table)                                                      |
| Postgres FTS  | ~5 ms         | ~2.7 ms        | ~180 MB    | No             | 3/5 (You need to handle specific vector columns and indexes for performance)                 |
| Postgres TRGM | ~180 ms       | ~ 900 ms       | ~200 MB    | Yes            | 4/5 (You just generate indexes on the columns you need)                                      |
| Redis Search  | ~0.4 ms       | ~ 0.45 ms      | ~180 MB    | Yes            | 4/5 (You need to generate index manually and update it based on your data)                   |
| Meilisearch   | ~4.8 ms       | ~4 ms          | ~300 MB    | Yes            | 5/5 (To start you don't even have to create index, It generates it by first add_document :D) |
| Apache Solr   | ~3 ms         | ~3.5 ms        | ~800 MB    | Yes            | 4/5 (Still easy but for real usage you might need zookeeper)                                 |

## 🚀 Quick Start

```bash
# Start all search systems
docker-compose up -d

# Or just start subset of search systems
docker-compose up -d redis postgres

# Setup environment
uv venv
uv pip install -r requirements.txt

# Run benchmarks
uv run -m app.benchmark

# Run single benchmark
uv run -m app.benchmark_single
```
