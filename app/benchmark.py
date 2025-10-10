import time
import asyncio
import json
import math


# Placeholder async search functions - define these as needed
async def postgres_search(query: str):
    pass  # Implement PostgreSQL FTS search


async def redis_search(query: str):
    pass  # Implement Redis search


async def elasticsearch_search(query: str):
    pass  # Implement Elasticsearch search


# BenchmarkResult would be a dict in Python


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
    systems = [
        {"name": "PostgreSQL FTS", "search": postgres_search},
        {"name": "Redis", "search": redis_search},
        {"name": "Elasticsearch", "search": elasticsearch_search},
        # ... more systems
    ]

    queries = [
        "laptop",
        "wireless gaming mouse",
        "laptp",  # typo
        # ... more queries
    ]

    results = []

    for system in systems:
        for query in queries:
            print(f"Benchmarking {system['name']} with query: {query}")
            latencies = await benchmark_query(system["search"], query)

            avg_latency = sum(latencies) / len(latencies) if latencies else 0
            throughput = 1000 / avg_latency if avg_latency > 0 else 0

            results.append(
                {
                    "system": system["name"],
                    "query": query,
                    "latencies": latencies,
                    "p50": calculate_percentile(latencies, 50),
                    "p95": calculate_percentile(latencies, 95),
                    "p99": calculate_percentile(latencies, 99),
                    "throughput": throughput,
                }
            )

    # Save results
    with open("results/latency.json", "w") as f:
        json.dump(results, f, indent=2)


# To run the benchmarks
if __name__ == "__main__":
    asyncio.run(run_benchmarks())
