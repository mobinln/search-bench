import time
import typesense
from typing import List
from dataclasses import asdict

from app.integrations.search_engine import SearchEngine, Product, Any

MEILISEARCH_URL = "http://127.0.0.1:7700"
MASTER_KEY = "some-key-here"


class TypesenseEngine(SearchEngine):
    def __init__(self):
        super().__init__()

        self.client = typesense.Client(
            {
                "nodes": [
                    {
                        "host": "localhost",
                        "port": "8108",
                        "protocol": "http",
                    }
                ],
                "api_key": "xyz",
                "connection_timeout_seconds": 2,
            }
        )

        schema = {
            "name": "products",
            "fields": [
                {"name": "id", "type": "string"},
                {"name": "name", "type": "string"},
                {"name": "description", "type": "string"},
                {"name": "category", "type": "string"},
                {"name": "brand", "type": "string"},
                {"name": "rating", "type": "float"},
            ],
            "default_sorting_field": "rating",
        }

        try:
            self.client.collections["products"].delete()
        except Exception as e:
            print("Error on delete index :", e)

        try:
            self.client.collections.create(schema)
        except Exception as e:
            print("Error on create index :", e)

    def ingest_data(self, data):
        print("ingesting data")
        self.client.collections["products"].documents.import_([asdict(i) for i in data])

        time.sleep(5)

    async def search(self, query):
        print("searching:", query)
        return self.client.collections["products"].documents.search(
            {
                "q": query,
                "query_by": "name",
            }
        )

    def close(self):
        return super().close()
