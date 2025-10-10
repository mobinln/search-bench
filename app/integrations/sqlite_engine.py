import sqlite3
from typing import List
from app.integrations.search_engine import SearchEngine, Product, Any


class SqliteSearchEngine(SearchEngine):
    def __init__(self):
        super().__init__()
        self.db = sqlite3.connect(":memory:")
        self.cursor = self.db.cursor()

        self.cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS products USING fts5(
                id,
                name,
                description,
                category,
                brand,
                price,
                rating,
                stock,
                tags,
                tokenize = 'porter ascii'
            )
        """)

    def ingest_data(self, data: List[Product]) -> None:
        """Ingest a list of products into the index."""
        self.cursor.executemany(
            """INSERT INTO products(id, name, description, category, brand, price, rating, stock, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""",
            [
                (
                    i.id,
                    i.name,
                    i.description,
                    i.category,
                    i.brand,
                    i.price,
                    i.rating,
                    i.stock,
                    ",".join(i.tags),
                )
                for i in data
            ],
        )
        self.db.commit()

    async def search(self, query: str) -> Any:
        """Search the index asynchronously."""
        self.cursor.execute(
            "SELECT id, name, description FROM products WHERE products MATCH ?", [query]
        )
        return self.cursor.fetchall()

    async def close(self):
        await super().close()
        self.db.close()
