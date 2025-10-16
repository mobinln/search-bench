import asyncio
import time
import plotly.express as px

from app.integrations.redis_engine import RedisSearchEngine
from app.data_generator import generate_data, generate_query


async def run():
    engine = RedisSearchEngine()

    data = generate_data(1 * 1000 * 1000)
    print("data generated")

    batch_size = 100 * 1000

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

    try:
        await engine.close()
    except:
        pass

    print(f"Found {len(result)} results")
    print(f"Took {latencies[-1]:.4f} ms")

    fig = px.line(x=[i for i in range(len(latencies))], y=latencies, title="Latency")
    fig.show()


asyncio.run(run())
