import logging
from sys import stdout

# Init logger
logging.basicConfig(stream=stdout, level=logging.INFO)
logger = logging.getLogger(name=__name__)


def get_event_uri(event: dict):
    """
    Parse the given event & extract the web URI to use as the message key
    """
    try:
        uri = event.get("meta").get("uri")

        return uri
    except Exception as ex:
        logger.error(f"Cannot retrieve event URI for key assignment due to: {ex}")
        raise RuntimeError(f"Cannot retrieve event URI for key assignment due to: {ex}")
