"""Output data."""
from pathlib import Path
import dataclasses
import json
import logging
import os
from google.cloud import pubsub_v1

logger = logging.getLogger(__name__)
DATA_PATH = Path(os.environ["DATA_PATH"])

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path("data-engineering", "purchases")
try:
    publisher.create_topic(request={"name": topic_path})
except:
    pass


def dump_files(data, dir_):
    """Dump data to disk.

    :param data:    The data to dump.
    :param dir_:    Directory name in which to store the data.
    """
    data_path = DATA_PATH / dir_
    logger.info("Dump %d files to %s.", len(data), data_path)
    data_path.mkdir(parents=True, exist_ok=True)

    for d in data:
        with open(data_path / f"{d.id_}.json", "w", encoding="utf8") as json_file:
            json.dump(dataclasses.asdict(d), json_file)


def publish(data):
    """Publish data to pubsub topic.

    :param data:    The list of data to publish.
    """
    logger.info("Publish %d events to %s.", len(data), topic_path)
    for d in data:
        publisher.publish(topic_path, json.dumps(dataclasses.asdict(d)).encode("utf-8"))
