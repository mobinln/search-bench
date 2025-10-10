import asyncio
import time
import plotly.express as px

from app.integrations.sqlite_engine import SqliteSearchEngine
from app.integrations.postgres_fts_engine import PostgresFtsSearchEngine
from app.integrations.postgres_trgm_engine import PostgresTrgmSearchEngine
from app.data_generator import generate_data


async def run():
    sq = SqliteSearchEngine()
    # sq = PostgresFtsSearchEngine()
    # sq = PostgresTrgmSearchEngine()

    data = generate_data(10 * 1000)

    sq.ingest_data(data)

    latencies = []
    for i in range(20):
        start = time.time()
        result = await sq.search("Nike")
        end = time.time()
        latency = (end - start) * 1000
        latencies.append(latency)

    print(f"Found {len(result)} results")
    print(f"Took {latencies[-1]:.4f} ms")

    fig = px.line(x=[i for i in range(len(latencies))], y=latencies, title="Latency")
    fig.show()


asyncio.run(run())
