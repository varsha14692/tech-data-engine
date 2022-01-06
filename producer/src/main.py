"""Produce data events."""
import logging
from data import articles, purchases, users

logger = logging.getLogger(__name__)


def produce() -> None:
    """Generate events."""
    logger.info("Start producing events.")
    article_ids = articles.main()
    user_ids = users.main()

    purchases.main(user_ids, article_ids)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    produce()
