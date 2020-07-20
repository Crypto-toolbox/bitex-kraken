from typing import Optional, Union

import bitex.plugins.base import hookimpl
from bitex_kraken.constants import VERSIONED_API_URL, PUBLIC_ENDPOINTS


def determine_endpoint_type(endpoint: str) -> str:
    if endpoint not in PUBLIC_ENDPOINTS:
        return "private"
    return "public"


def build_kraken_endpoint(instrument, endpoint, action: Optional[str] = None) -> Union[str, Tuple[str, Dict[str, str]]]:
    """Construct a valid Kraken endpoint from the given args.

    Example::

        >>>build_kraken_endpoint("XBTUSD", "Trades")
        "/Trades?pair=XXBTZUSD"
        >>>build_kraken_endpoint("XBTUSD", "Order", "create")
        ("/AddOrder", {"pair": "XXBTZUSD"})
        >>>build_kraken_endpoint("XBTUSD", "Order", "cancel")
        ("/CancelOrder", {"pair": "XXBTZUSD"})
    """


@hookimpl
def construct_url_from_shorthand(matchdict):
    """construct the url from shorthand.

    The `matchdict` object has the following layout::

        >>>matchdict
        {
            "exchange": str(),
            "instrument": str(),
            "endpoint": str(),
            "action": str() or None,
        }

    """
    exchange = matchdict["exchange"]
    instrument = matchdict["instrument"]
    endpoint = matchdict["endpoint"]
    action = matchdict.get("action")

    endpoint_type = determine_endpoint_type(endpoint)

    return f"{VERSIONED_API_URL}/{endpoint_type}/{endpoint}"