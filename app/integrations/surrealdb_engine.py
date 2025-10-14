import time
from surrealdb import Surreal
from typing import List
from dataclasses import asdict

from app.integrations.search_engine import SearchEngine, Product, Any


class SurrealdbEngine(SearchEngine):
    def __init__(self):
        super().__init__()

        with Surreal("ws://localhost:8000/rpc") as db:
            db.signin({"username": "root", "password": "root"})
            db.use("my_namespace", "my_db")

            db.query("""
            DEFINE ANALYZER my_analyzer
            TOKENIZERS class, blank
            FILTERS lowercase, ascii;
            """)

            db.delete("products")
            db.query("DEFINE TABLE products SCHEMALESS;")

            db.query("""
                DEFINE INDEX fts_name ON TABLE products COLUMNS name SEARCH ANALYZER my_analyzer BM25 HIGHLIGHTS;
            """)

    def ingest_data(self, data):
        print("ingesting data")
        with Surreal("ws://localhost:8000/rpc") as db:
            db.signin({"username": "root", "password": "root"})
            db.use("my_namespace", "my_db")

            for doc in data:
                db.create("products", asdict(doc))

    async def search(self, query):
        print("searching:", query)
        with Surreal("ws://localhost:8000/rpc") as db:
            db.signin({"username": "root", "password": "root"})
            db.use("my_namespace", "my_db")

            return db.query(f"""
        SELECT id, name, description, category, brand,
          search::score(0) + search::score(1) AS score
        FROM products
        WHERE
            name @@ "{query}" OR description @@ "{query}" OR
            category @@ "{query}" OR brand @@ "{query}"
        ORDER BY score DESC
        LIMIT 10;
        """)

    def close(self):
        return super().close()
