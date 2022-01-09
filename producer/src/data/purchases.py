"""Generate and dump purchase event data."""
from datetime import datetime
from uuid import uuid4
from typing import List
import dataclasses
import logging
import random
import db
import time
import output
from faker import Faker

DATA_DIR = "purchases"
logger = logging.getLogger(__name__)
faker = Faker()


@dataclasses.dataclass
class CartItem:
    """Basic User."""

    article_id: str
    quantity: int


@dataclasses.dataclass
class Purchase:
    """Basic Purchase."""

    id_: str
    timestamp: str
    user_id: str
    cart: List[CartItem]

@dataclasses.dataclass
class Purchases:
    """Custom Purchase."""

    id_: str
    timestamp: str
    user_id: str
    article_id: str
    quantity: int


def _generate_purchase(user_ids: List[str], article_ids: List[str]) -> Purchase:
    """Generate a random purchase.

    :param user_ids:    List of user ids.
    :param article_ids: List of article ids.
    :returns:           Generated purchase.
    """
    logging.debug("Generate purchase event.")

    return Purchase(
        id_=str(uuid4()),
        timestamp=datetime.now().isoformat(),
        user_id=random.sample(user_ids, 1)[0],
        cart=[
            CartItem(
                article_id=random.sample(article_ids, 1)[0],
                quantity=random.randint(1, 5),
            )
            for _ in range(random.randint(1, 4))
        ],
    )


def _sink(purchaseList: List[Purchase]) -> None:
    """Sink generated purchase data to disk and publish to topic.

    :param purchase:   The purchase data to sink.
    """
    purchases: List[Purchases]=[]       
    output.dump_files(purchaseList, DATA_DIR)
    output.publish(purchaseList)
    logger.info("purchaseList %s data before object construction.", purchaseList)
    for purchase in purchaseList:
        for cartItem in purchase.cart:
            purchases.append(Purchases(
            id_=purchase.id_,
            timestamp=purchase.timestamp,
            user_id=purchase.user_id,
            article_id=cartItem.article_id,
            quantity=cartItem.quantity
            ))
    
    db.insert_records(purchases, DATA_DIR)
    logger.info("purchases data inserted successfully .")

def _sleep() -> None:
    """Sleep."""
    sleep = random.randrange(1, 3)
    logger.info("Sleep %s seconds.", sleep)
    time.sleep(sleep)


def _invalidate(event: Purchase) -> Purchase:
    """Make some of the data invalid.

    :param event:   Data to invalidate
    """
    logger.debug("Invalidate an event.")
    randomizer = random.random()

    if randomizer < 0.2:
        event.user_id = str(uuid4())

    elif randomizer < 0.4:
        event.cart = faker.words(random.randint(0, 10))

    elif randomizer < 0.6:
        event.cart = []

    elif randomizer < 0.8:
        random.choice(event.cart).article_id = str(uuid4())

    else:
        random.choice(event.cart).quantity = random.randint(-30, -4)

    return event


def _batch_generate(user_ids: List[str], article_ids: List[str]) -> List[Purchase]:
    """Generate between 1 and 9 events.

    :param user_ids:    List of user ids.
    :param article_ids: List of article ids.
    """
    nbr_events = random.randrange(1, 9)

    logger.info("Generate %s purchase events.", nbr_events)
    events = [_generate_purchase(user_ids, article_ids) for _ in range(nbr_events)]

    return [e if random.random() > 0.15 else _invalidate(e) for e in events]


def main(user_ids: List[str], article_ids: List[str]) -> None:
    """Generate and dump purchase event data.

    :param user_ids:    List of user ids.
    :param article_ids: List of article ids.
    """
    while True:
        _sleep()
        _sink(_batch_generate(user_ids, article_ids))
