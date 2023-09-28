import logging
from sys import stdout
from confluent_kafka import Producer

# Init logger
logging.basicConfig(stream=stdout, level=logging.INFO)
logger = logging.getLogger(name=__name__)

# Callback function - used to ensure message delivery
def delivery_callback(err_msg, msg):
    # If no error message, log our success
    if not err_msg:
        logger.info(f"Message successfully sent with key: {msg.key()}, to topic: {msg.topic()}, at partition: {msg.partition()} & with offset {msg.offset()}.")
    else:
        logger.error(f"Message unsuccessfully sent with error message: {err_msg}.")

def produce_data(producer: Producer, key: str, topic_name: str, data: bytes, callback=delivery_callback):
    """
    Produce data to a given topic

    """
    return producer.produce(topic=topic_name, key=key, value=data, on_delivery=callback)