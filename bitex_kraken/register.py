from typing import Union, Dict, Tuple, Optional

from bitex.plugins.base import hookimpl

from bitex_kraken.auth import KrakenAuth
from bitex_kraken.constants import EXCHANGE_NAME
from bitex_kraken.request import KrakenPreparedRequest
from bitex_kraken.response import KrakenResponse


@hookimpl
def announce_plugin():
    return EXCHANGE_NAME, KrakenAuth, KrakenPreparedRequest, KrakenResponse
