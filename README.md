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
- Duckdb Full-Text Search

## 📊 Key Findings

- **Fastest**: Redis Search (By far !!)
- **Best relevance**: Apache Solr or Meilisearch or Typesense
- **Easiest setup**: Meilisearch
- **Lowest resource usage**: Sqlite FTS5
- **Best for <10k docs**: Redis Search
- **Best for <100k docs**: Redis Search
- **Best for >1M docs**: Apache Solr or Meilisearch or Redis Search

| Engine        | Latency (10k) | Latency (100k) | RAM (100k) | Latency (1M) | Ease of use     |
| ------------- | ------------- | -------------- | ---------- | ------------ | --------------- |
| Sqlite FTS5   | ~1.8 ms       | ~0.8 ms        | ~150 MB    | ~5.5 ms      | ⭐️⭐️⭐️⭐️    |
| Postgres FTS  | ~5 ms         | ~2.7 ms        | ~180 MB    | ~27 ms       | ⭐️⭐️⭐️       |
| Postgres TRGM | ~180 ms       | ~ 900 ms       | ~200 MB    | ~6000 ms     | ⭐️⭐️⭐️       |
| Redis Search  | ~0.4 ms       | ~ 0.45 ms      | ~180 MB    | ~1.3 ms      | ⭐️⭐️⭐️       |
| Meilisearch   | ~4.8 ms       | ~4 ms          | ~300 MB    | ~12.5 ms     | ⭐️⭐️⭐️⭐️⭐️ |
| Apache Solr   | ~3 ms         | ~3.5 ms        | ~800 MB    | ~3.9 ms      | ⭐️⭐️⭐️⭐️    |
| Typesense     | ~4 ms         | ~4 ms          | ~280 MB    | ~10 ms       | ⭐️⭐️⭐️⭐️    |
| SurrealDB     | ~25 ms        | ~25 ms         | ~700 MB    | ~34 ms       | ⭐️⭐️⭐️       |
| Duckdb        | ~10.1 ms      | ~20 ms         | ~500 MB    | ~67 ms       | ⭐️⭐️⭐️       |

## 📌 Features

| Engine        | Typo Tolerance | Features                                                                     |
| ------------- | -------------- | ---------------------------------------------------------------------------- |
| Sqlite FTS5   | No             | Installed natively on python and most languages                              |
| Postgres FTS  | No             | Easy to setup and fast enough                                                |
| Postgres TRGM | Yes            | Typo tolerance but very slow                                                 |
| Redis Search  | Yes            | Super fast and easy                                                          |
| Meilisearch   | Yes            | Super easy to setup with ai search and faceted search and multi index search |
| Apache Solr   | Yes            | Very good scalability and also very fast and consistent                      |
| Typesense     | Yes            | Fast with good embedding search support and good docs                        |
| SurrealDB     | Yes            | Good features set like graphs and vectors but very slow ingestion            |
| Duckdb        | No             | Super fast data ingestion, good for analytics                                |

## 🤔 Conclusion

So which one should I use? well it depends, generally I don't recommend **Postgres TRGM** because as much as I saw in my tests
it is very slow but anyway if your stack is heavily integrated with postgres and you just want to add a search, Why not? use it it
is robust and typo tolerant, But if you want to use a dedicated search engine (cool) I guess **Redis Search** and **Apache Solr** are
the best options, **Redis Search** is so fast that I taught it is not working :D, And it actually works the search outputs are
actually solid, **Apache Solr** is a very scalable and famous option which uses **Apache Lucene** behind the scenes which is a
fast and robust search engine powering **Elasticsearch** and **OpenSearch** too, So for scalability the best by far is **Apache Solr**.
For ease of use and prototyping and even small to medium load the best option is **Meilisearch**, Easy to start, Easy to work and
very good feature set out of the box, and finally if you need an embedded search/ filter engine to pre-process or even process data
your best options are **Sqlite** and **Duckdb**, They are very easy to work and use low overhead and they can ingest and process huge
amounts of data very fast with low resource usage.

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
