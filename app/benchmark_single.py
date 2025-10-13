import asyncio
import time
import plotly.express as px

from app.integrations.sqlite_engine import SqliteSearchEngine
from app.integrations.postgres_fts_engine import PostgresFtsSearchEngine
from app.integrations.postgres_trgm_engine import PostgresTrgmSearchEngine
from app.integrations.redis_engine import RedisSearchEngine
from app.integrations.meilisearch_engine import MeilisearchEngine
from app.integrations.solr_engine import SolrEngine
from app.data_generator import generate_data, generate_query


async def run():
    # engine = SqliteSearchEngine()
    # engine = PostgresFtsSearchEngine()
    # engine = PostgresTrgmSearchEngine()
    # engine = RedisSearchEngine()
    # engine = MeilisearchEngine()
    engine = SolrEngine()

    data = generate_data(100 * 1000)

    engine.ingest_data(data)

    latencies = []
    for i in range(100):
        query = generate_query()

        start = time.time()
        result = await engine.search(query)
        end = time.time()
        latency = (end - start) * 1000
        latencies.append(latency)

    engine.close()
    print(f"Found {len(result)} results")
    print(f"Took {latencies[-1]:.4f} ms")

    fig = px.line(x=[i for i in range(len(latencies))], y=latencies, title="Latency")
    fig.show()


asyncio.run(run())
