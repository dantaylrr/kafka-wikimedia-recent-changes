import logging
from sys import stdout
from requests import Session
from requests.adapters import Retry, HTTPAdapter
from sseclient import SSEClient

# Instantiate logger
logging.basicConfig(stream=stdout, level=logging.INFO)
logger = logging.getLogger(name=__name__)

def _generate_headers():
    """
    Generate content headers for API request.
    """
    return {'Content-type': 'text/event-stream'}

def _mount_endpoint():
    """
    Mount the URL endpoint as a requests session so that we can re-use it throughout the application &
    retry throughout.
    """
    try:
        # Initialise a session
        req_session = Session()
        # Mount our retry strategy onto the session
        req_session.mount(
            prefix="https://", adapter=HTTPAdapter(max_retries=Retry(total=5, status_forcelist=[500, 501, 502, 503, 504]))
        )

        # Return the session for re-usability throughout code
        return req_session
    except Exception as ex:
        logger.warning(
            f"Failure to successfully mount endpoint with retry strategy: {ex} - allowing application to continue..."
        )

def stream_data(session: Session = _mount_endpoint()):
    """
    Issue a GET request to the recent changes endpoint.
    This creates a generator object that will continue to refresh / get the latest data.
    We can then iterate through this generator object & process each event.
    """
    try:
        # Get API response
        stream_source = session.get(url='https://stream.wikimedia.org/v2/stream/recentchange', stream=True, headers=_generate_headers())

        # Return generator object / client
        return SSEClient(event_source=stream_source)

    except Exception as ex:
        logger.warning(
            f"Failure to successfully stream recent change events from wikimedia endpoint: {ex} - exiting application..."
        )
        raise RuntimeError("Exiting...")