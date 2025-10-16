import time
import asyncio
import json
import math
from typing import List

from app.integrations.search_engine import SearchEngine
from app.data_generator import generate_data, queries

from app.integrations.sqlite_engine import SqliteSearchEngine
from app.integrations.postgres_fts_engine import PostgresFtsSearchEngine
from app.integrations.postgres_trgm_engine import PostgresTrgmSearchEngine
from app.integrations.redis_engine import RedisSearchEngine


async def benchmark_query(search_fn, query: str, iterations: int = 1000) -> list[float]:
    latencies: list[float] = []

    # Warmup
    for _ in range(100):
        await search_fn(query)

    # Actual benchmark
    for _ in range(iterations):
        start = time.perf_counter()
        await search_fn(query)
        end = time.perf_counter()
        latencies.append((end - start) * 1000)  # Convert to milliseconds

    latencies.sort()
    return latencies


def calculate_percentile(sorted_latencies: list[float], percentile: float) -> float:
    index = math.ceil((percentile / 100) * len(sorted_latencies)) - 1
    return sorted_latencies[index]


# Run against all systems
async def run_benchmarks():
    systems: List[SearchEngine] = [
        SqliteSearchEngine,
        PostgresFtsSearchEngine,
        PostgresTrgmSearchEngine,
        RedisSearchEngine,
    ]

    data = generate_data(10 * 1000)

    results = []

    for system in systems:
        engine = system()
        engine.ingest_data(data)

        for query in queries:
            print(f"Benchmarking {type(engine).__name__} with query: {query}")
            latencies = await benchmark_query(engine.search, query)

            avg_latency = sum(latencies) / len(latencies) if latencies else 0
            throughput = 1000 / avg_latency if avg_latency > 0 else 0

            results.append(
                {
                    "system": type(engine).__name__,
                    "query": query,
                    "p50": calculate_percentile(latencies, 50),
                    "p95": calculate_percentile(latencies, 95),
                    "p99": calculate_percentile(latencies, 99),
                    "throughput": throughput,
                }
            )

        engine.close()

    # Save results
    with open("./latency.json", "w") as f:
        json.dump(results, f, indent=2)


# To run the benchmarks
if __name__ == "__main__":
    asyncio.run(run_benchmarks())
