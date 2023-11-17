import logging
import os
from sys import stdout
import json

from confluent_kafka import Producer

from rcp_utils.kafka.produce_data import produce_data
from rcp_utils.kafka.get_uri import get_event_uri
from rcp_utils.api.api_utils import stream_data

# Initialise the logger
logging.basicConfig(stream=stdout, level=logging.INFO)
logger = logging.getLogger(name=__name__)

LOCAL_IP = os.environ["LOCAL_IP"]


def main():
    """
    Entry point into the consumer application.

    Will mount the Wikipedia recent changes URL & begin to consume from it using requests library
    Will produce messages into local kafka topic, ready for consumption.
    """
    logger.info("Starting application...")

    # Define kafka configuration properties
    k_conf = {
        "bootstrap.servers": f"{LOCAL_IP}:9092",
    }

    # Init producer class
    producer = Producer(k_conf)

    # Get the data events generator object
    streamed_events = stream_data()

    """
    Loop through our generator object & process each event - for examples sake, I will use the
    web URI as the kafka key.
    Although this isn't necessary & likely won't impact how messages are sent, I want to follow best
    practices & use keys where possible.
    """
    while True:
        try:
            for event in streamed_events.events():
                event_content = json.loads(event.data)
                # Get the event URI for message key assignment
                uri = get_event_uri(event=event_content)

                # Produce the event to the relevant Kafka topic
                produce_data(
                    producer=producer,
                    key=uri,
                    topic_name="wikimedia-changes",
                    data=bytes(json.dumps(event_content).encode("utf-8")),
                )

        except KeyboardInterrupt:
            break

    # Flush the producer of messages
    producer.flush()


if __name__ == "__main__":
    main()
