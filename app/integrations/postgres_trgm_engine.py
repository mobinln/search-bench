import psycopg2
from psycopg2.extras import RealDictCursor
from app.integrations.search_engine import SearchEngine

# Database connection parameters
# Adjust these to match your PostgreSQL setup
DB_CONFIG = {
    "dbname": "mydb",
    "user": "myuser",
    "password": "mypassword",
    "host": "localhost",
    "port": "5432",
}


class PostgresTrgmSearchEngine(SearchEngine):
    def __init__(self):
        super().__init__()
        self.db = psycopg2.connect(**DB_CONFIG)
        self.cursor = self.db.cursor(cursor_factory=RealDictCursor)

        self.cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

        self.cursor.execute("DROP TABLE IF EXISTS products")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                brand TEXT NOT NULL,
                price DOUBLE PRECISION,
                rating DOUBLE PRECISION,
                stock NUMERIC,
                tags TEXT NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE INDEX products_name_trgm_idx ON products USING GIN (name gin_trgm_ops)
        """)

        self.cursor.execute("""
            CREATE INDEX products_description_trgm_idx ON products USING GIN (description gin_trgm_ops)
        """)

        self.cursor.execute("""
            CREATE INDEX products_brand_trgm_idx ON products USING GIN (brand gin_trgm_ops)
        """)

        self.db.commit()

    def ingest_data(self, data):
        super().ingest_data(data)

        self.cursor.executemany(
            """INSERT INTO products(id, name, description, category, brand, price, rating, stock, tags)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
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

    async def search(self, query):
        self.cursor.execute("SET pg_trgm.similarity_threshold = 0.3")

        self.cursor.execute(
            """
            SELECT name, description, brand, similarity(name, %s) AS score
            FROM products
            WHERE name %% %s OR brand %% %s OR description %% %s
            ORDER BY score DESC
            LIMIT 5
        """,
            [query, query, query, query],
        )

        return self.cursor.fetchall()

    async def close(self):
        await super().close()
        self.db.close()
