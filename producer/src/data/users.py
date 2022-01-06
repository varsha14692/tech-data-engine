"""Generate and dump user data."""
from dataclasses import dataclass
from typing import List
import logging
import db
import output
from faker import Faker

logger = logging.getLogger(__name__)
DATA_DIR = "users"
NBR_USERS = 1000


@dataclass
class User:
    """Basic User."""

    id_: str
    name: str
    address: str
    number: str
    email: str


def _generate_user(gen: Faker) -> User:
    """Generate a random user.

    :param gen: Faker generator.
    :return:    Generated user.
    """
    return User(
        id_=gen.uuid4(),
        name=gen.name(),
        address=gen.address(),
        number=gen.phone_number(),
        email=gen.email(),
    )


def _get_ids(users: List[User]) -> List[str]:
    """Get list of all user ids.

    :param users:   The user data.
    """
    return [user.id_ for user in users]


def _sink(users: List[User]) -> None:
    """Sink generated user data to disk and insert to db.

    :param users:   The user data to sink.
    """
    output.dump_files(users, DATA_DIR)
    db.insert_records(users, DATA_DIR)


def main() -> List[str]:
    """Generate and dump user data."""
    faker = Faker()

    logger.info("Generate %d users.", NBR_USERS)
    users = [_generate_user(faker) for _ in range(NBR_USERS)]
    _sink(users)

    return _get_ids(users)
