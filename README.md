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
- **Easiest setup**: TBD
- **Lowest resource usage**: TBD
- **Best for <100k docs**: TBD
- **Best for >1M docs**: TBD

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
