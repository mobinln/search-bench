import random
from faker import Faker

from app.integrations.search_engine import Product

fake = Faker()

categories = ["Electronics", "Clothing", "Home", "Sports", "Books"]
brands = ["Samsung", "Apple", "Nike", "Sony", "Dell", "HP"]


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
