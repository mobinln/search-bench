import redis
from redis.commands.json.path import Path
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.index_definition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from typing import List
from app.integrations.search_engine import SearchEngine, Product
from dataclasses import asdict


class RedisSearchEngine(SearchEngine):
    def __init__(self):
        super().__init__()
        self.redis = redis.Redis(decode_responses=True)

        self.schema = (
            TextField("$.name", as_name="name"),
            TextField("$.description", as_name="description"),
            TagField("$.category", as_name="category"),
            TagField("$.brand", as_name="brand"),
            NumericField("$.stock", as_name="stock"),
            NumericField("$.price", as_name="price"),
            NumericField("$.rating", as_name="rating"),
            TagField("$.tags[*]", as_name="tags"),
        )

        self.redis.flushall()
        try:
            self.redis.ft("idx:products").create_index(
                self.schema,
                definition=IndexDefinition(
                    prefix=["products:"], index_type=IndexType.JSON
                ),
            )
        except Exception as e:
            print("Index might already exists:", e)

    def ingest_data(self, data: List[Product]) -> None:
        pipe = self.redis.pipeline()

        for doc in data:
            key = doc.id
            content = {k: v for k, v in asdict(doc).items() if k != "id"}
            pipe.json().set(f"products:{key}", "$", content)

        pipe.execute()

    async def search(self, query):
        return self.redis.ft("idx:products").search(Query(query)).docs

    def close(self):
        self.redis.close()
