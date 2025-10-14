import asyncio
import time
import plotly.express as px

from app.integrations.sqlite_engine import SqliteSearchEngine
from app.integrations.postgres_fts_engine import PostgresFtsSearchEngine
from app.integrations.postgres_trgm_engine import PostgresTrgmSearchEngine
from app.integrations.redis_engine import RedisSearchEngine
from app.integrations.meilisearch_engine import MeilisearchEngine
from app.integrations.solr_engine import SolrEngine
from app.integrations.typesense_engine import TypesenseEngine
from app.integrations.surrealdb_engine import SurrealdbEngine
from app.data_generator import generate_data, generate_query


async def run():
    # engine = SqliteSearchEngine()
    # engine = PostgresFtsSearchEngine()
    # engine = PostgresTrgmSearchEngine()
    # engine = RedisSearchEngine()
    engine = MeilisearchEngine()
    # engine = SolrEngine()
    # engine = TypesenseEngine()
    # engine = SurrealdbEngine()

    data = generate_data(1 * 1000 * 1000)
    print("data generated")

    batch_size = 50 * 1000

    for i in range(0, len(data), batch_size):
        batch = data[i : i + batch_size]
        engine.ingest_data(batch)

    print("data ingested")

    latencies = []
    for i in range(100):
        query = generate_query()

        start = time.time()
        result = await engine.search(query)
        end = time.time()
        latency = (end - start) * 1000
        latencies.append(latency)

    await engine.close()
    print(f"Found {len(result)} results")
    print(f"Took {latencies[-1]:.4f} ms")

    fig = px.line(x=[i for i in range(len(latencies))], y=latencies, title="Latency")
    fig.show()


asyncio.run(run())
