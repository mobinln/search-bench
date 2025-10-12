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


class PostgresFtsSearchEngine(SearchEngine):
    def __init__(self):
        super().__init__()
        self.db = psycopg2.connect(**DB_CONFIG)
        self.cursor = self.db.cursor(cursor_factory=RealDictCursor)

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
                tags TEXT NOT NULL,
                search_vector tsvector
            )
        """)

        self.cursor.execute("""
            CREATE INDEX products_search_idx ON products USING GIN(search_vector)
        """)

        # Create a trigger to automatically update search_vector on INSERT/UPDATE
        self.cursor.execute("""
            CREATE OR REPLACE FUNCTION products_search_trigger() RETURNS trigger AS $$
            BEGIN
                NEW.search_vector :=
                    setweight(to_tsvector('english', coalesce(NEW.name, '')), 'A') ||
                    setweight(to_tsvector('english', coalesce(NEW.description, '')), 'B') ||
                    setweight(to_tsvector('english', coalesce(NEW.category, '')), 'C') ||
                    setweight(to_tsvector('english', coalesce(NEW.brand, '')), 'D');
                RETURN NEW;
            END
            $$ LANGUAGE plpgsql;
            
            CREATE TRIGGER tsvector_update BEFORE INSERT OR UPDATE
            ON products FOR EACH ROW EXECUTE FUNCTION products_search_trigger();
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
        self.cursor.execute(
            """
            SELECT name, description, category
            FROM products
            WHERE search_vector @@ to_tsquery('english', %s)
        """,
            [" & ".join(query.split())],
        )

        return self.cursor.fetchall()

    async def close(self):
        await super().close()
        self.db.close()
