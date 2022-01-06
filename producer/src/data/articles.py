"""Generate and dump article data."""
from dataclasses import dataclass
from typing import List
import logging
import random
import db
import output
from faker import Faker

logger = logging.getLogger(__name__)
DATA_DIR = "articles"
NBR_ARTICLES = 200
CURRENCIES = ["USD", "SEK", "EUR"]


@dataclass
class Article:
    """Basic Article."""

    id_: str
    name: str
    price: float
    currency: str


def _generate_article(gen: Faker) -> Article:
    """Generate a random article.

    :param gen: Faker generator.
    :return:    Generated product.
    """
    return Article(
        id_=gen.uuid4(),
        name=" ".join(gen.words(random.randint(1, 3))).capitalize(),
        price=round(random.uniform(0, 400), 2),
        currency=random.sample(CURRENCIES, 1)[0],
    )


def _sink(articles: List[Article]) -> None:
    """Process generated article data.

    :param articles:   The article data to process.
    """
    output.dump_files(articles, DATA_DIR)
    db.insert_records(articles, DATA_DIR)


def _get_ids(articles: List[Article]) -> List[str]:
    """Get list of all article ids.

    :param articles:    The article data.
    """
    return [article.id_ for article in articles]


def main() -> List[str]:
    """Generate and dump article data."""
    faker = Faker()

    logger.info("Generate %d articles.", NBR_ARTICLES)
    articles = [_generate_article(faker) for _ in range(NBR_ARTICLES)]
    _sink(articles)

    return _get_ids(articles)
