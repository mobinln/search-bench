from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Any


@dataclass
class Product:
    id: str
    name: str
    description: str
    category: str
    brand: str
    stock: int
    price: float
    rating: float
    tags: List[str]


class SearchEngine(ABC):
    """Abstract base for an index-like system."""

    @abstractmethod
    def ingest_data(self, data: List[Product]) -> None:
        """Ingest a list of products into the index."""
        pass

    @abstractmethod
    async def search(self, query: str) -> Any:
        """Search the index asynchronously."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Closes the connection and cleans up resources."""
        pass
