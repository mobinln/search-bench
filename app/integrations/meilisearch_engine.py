import time
import meilisearch
from typing import List
from dataclasses import asdict

from app.integrations.search_engine import SearchEngine, Product, Any

MEILISEARCH_URL = "http://127.0.0.1:7700"
MASTER_KEY = "some-key-here"


class MeilisearchEngine(SearchEngine):
    def __init__(self):
        super().__init__()

        self.client = meilisearch.Client(MEILISEARCH_URL, MASTER_KEY)

        self.client.delete_index("products")
        self.index = self.client.index("products")

    def ingest_data(self, data):
        self.index.add_documents([asdict(i) for i in data])
        time.sleep(5)

    async def search(self, query):
        return self.index.search(query)

    def close(self):
        return super().close()
