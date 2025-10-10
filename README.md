# Search Systems Benchmark

A comprehensive comparison of different search approaches for product search,
with real benchmarks and interactive demos.

## 🎯 Goal

When building an application that needs search, which system should you use?
This project benchmarks and compares multiple different approaches across latency,
relevance, features, and operational complexity.

## 🔍 Systems Compared

- SQLite FTS5
- PostgreSQL Full-Text Search
- PostgreSQL with pg_trgm (trigrams)
- Redis with RediSearch
- Apache Solr
- Meilisearch

## 📊 Key Findings

- **Fastest**: TBD
- **Best relevance**: TBD
- **Easiest setup**: Sqlite FTS5
- **Lowest resource usage**: Sqlite FTS5
- **Best for <10k docs**: TBD
- **Best for <100k docs**: TBD
- **Best for >1M docs**: TBD

_Speed column is calculated on a 10k dataset_

| Engine        | Speed   | Typo Tolerance | Ease of setup and use                                                                  |
| ------------- | ------- | -------------- | -------------------------------------------------------------------------------------- |
| Sqlite FTS5   | ~1.8 ms | No             | 5/5 (You only create a VIRTUAL table and it indexes all columns, much like a nosql db) |
| Postgres FTS  | ~5 ms   | No             | 3/5 (You need to handle specific vector columns and indexes for performance)           |
| Postgres TRGM | ~180 ms | Yes            | 4/5 (You just generate indexes on the columns you need)                                |

[Include charts here]

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

# See visualizations

```
