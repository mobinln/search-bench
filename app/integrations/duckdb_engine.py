import time
import duckdb
import pandas as pd
from typing import List
from dataclasses import asdict

from app.integrations.search_engine import SearchEngine, Product, Any


class DuckdbEngine(SearchEngine):
    def __init__(self):
        super().__init__()

        self.client = duckdb.connect()

        self.client.sql("DROP TABLE IF EXISTS products;")

        self.client.sql("""
        CREATE TABLE products (
            id VARCHAR,
            name VARCHAR,
            description VARCHAR,
            category VARCHAR,
            brand VARCHAR,
            price FLOAT,
            rating FLOAT,
            stock INTEGER,
            tags VARCHAR[]
        );""")

    def ingest_data(self, data):
        print("ingesting data")
        df = pd.DataFrame([asdict(i) for i in data])

        self.client.sql("INSERT INTO products SELECT * FROM df")

        try:
            self.client.execute("PRAGMA drop_fts_index(products);")
        except:
            pass
        self.client.execute("""
        PRAGMA create_fts_index(
            'products', 'id', 'name', 'description', 'category', 'brand'
        );""")

    async def search(self, query):
        print("searching:", query)

        return self.client.execute(f"""
            SELECT id, name, description, category, score
            FROM (
                SELECT *, fts_main_products.match_bm25(
                    id,
                    '{query}'
                ) AS score
                FROM products
            ) sq
            WHERE score IS NOT NULL
            LIMIT 20;
            """).fetchall()

    def close(self):
        self.client.close()
        return super().close()
