import time
import pysolr
from typing import List
from dataclasses import asdict

from app.integrations.search_engine import SearchEngine, Product, Any

SOLR_URL = "http://localhost:8983/solr/gettingstarted/"


class SolrEngine(SearchEngine):
    def __init__(self):
        super().__init__()

        self.client = pysolr.Solr(SOLR_URL, timeout=10)

        self.client.ping()
        print("connected to slor")

        self.client.delete(q="*:*", commit=True)

    def ingest_data(self, data):
        self.client.add([asdict(i) for i in data], commit=True)
        time.sleep(5)

    async def search(self, query):
        return self.client.search(query)

    def close(self):
        return super().close()
