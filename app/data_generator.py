import random
from faker import Faker

from app.integrations.search_engine import Product

fake = Faker()

categories = ["Electronics", "Clothing", "Home", "Sports", "Books"]
brands = ["Samsung", "Apple", "Nike", "Sony", "Dell", "HP"]

queries = [
    # General Keyword Searches
    "wireless headphones",
    "eco friendly laptop",
    "portable speaker",
    "premium smartwatch",
    "bestseller shoes",
    "smart home device",
    "sports watch",
    "running shoes",
    "gaming monitor",
    "wireless charger",
    # Category-Driven Queries
    "electronics under 500",
    "cheap sports gear",
    "home appliances",
    "clothing for men",
    "book about technology",
    "apple electronics",
    "nike sportswear",
    "sony headphones",
    "dell monitor",
    "hp laptop",
    # Natural-Language Queries
    "show me premium electronics",
    "best rated products",
    "eco friendly items under 100",
    "popular portable devices",
    "cheap wireless gadgets",
    "products with 5 star rating",
    "bestselling clothing",
    "what’s new in books",
    "laptops with good reviews",
    "high stock electronics",
    # Filter-Style Queries
    "laptops price 500 to 1000",
    "smartphones below 300",
    "sports gear under 50",
    "books over 4 stars",
    "wireless products above 4.5 rating",
    "eco-friendly premium devices",
    "apple products under 1000",
    "nike shoes size 42",
    "products in stock",
    "out of stock items",
    # Fuzzy / Typo-Tolerant Test Queries
    "samgsung phone",
    "ecofrendly",
    "wirless earbuds",
    "premum laptop",
    "sportz gear",
    "dall moniter",
    "sonny tv",
    "hp labtop",
    "bestsellar book",
    "potable speaker",
]


def generate_query():
    return random.choice(queries)


def generate_product():
    return Product(
        id=fake.uuid4(),
        name=fake.catch_phrase(),
        description=fake.text(max_nb_chars=200),
        category=random.choice(categories),
        brand=random.choice(brands),
        price=round(random.uniform(10, 2000), 2),
        rating=round(random.uniform(1, 5), 1),
        stock=random.randint(0, 1000),
        tags=random.sample(
            ["wireless", "portable", "premium", "eco-friendly", "bestseller"],
            k=random.randint(1, 3),
        ),
    )


def generate_data(count=100):
    return [generate_product() for _ in range(count)]
