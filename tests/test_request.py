# Built-in
from unittest.mock import MagicMock, patch
import json
# Third-party
import pytest
import responses

# Home-brew
from bitex import BitexSession
from bitex.plugins import list_loaded_plugins
from bitex_kraken import KrakenAuth, KrakenPreparedRequest, KrakenResponse

with open("tests/data/ticker.json") as f:
    ticker_json = json.load(f)

with open("tests/data/book.json") as f:
    book_json = json.load(f)

with open("tests/data/trades.json") as f:
    trades_json = json.load(f)


def test_plugin_was_loaded():
    loaded_plugins = list_loaded_plugins()
    assert "kraken" in loaded_plugins, "Plugin was not loaded!"
    assert loaded_plugins["kraken"] == {
        "Auth": KrakenAuth,
        "PreparedRequest": KrakenPreparedRequest,
        "Response": KrakenResponse
    }, "Plugin was loaded but is missing expected classes!"


class TestBitexRequest:

    @pytest.mark.parametrize(
        argnames="shorthand, expected_method, expected_url, expected_json",
        argvalues=[
            ("kraken://btcusd/ticker", responses.GET, "https://api.kraken.com/0/public/Ticker?pair=xbtusd",  ticker_json),
            ("kraken://btcusd/book", responses.GET, "https://api.kraken.com/0/public/Depth?pair=xbtusd",  book_json),
            ("kraken://btcusd/trades", responses.GET, "https://api.kraken.com/0/public/Trades?pair=xbtusd",  trades_json),
        ],
        ids=['ticker', "book", "trades"]
    )
    @responses.activate
    def test_standardized_method_is_implemented(self, shorthand, expected_method, expected_url, expected_json):
        responses.add(expected_method, expected_url, json=expected_json)

        session = BitexSession()
        resp = session.get(shorthand)

        assert len(responses.calls) == 1, "No requests were made to responses object!"
        assert responses.calls[0].request.url == expected_url, f"Unexpected request made to {responses.calls[0].request.url}"
        assert responses.calls[0].response.text == json.dumps(expected_json), f"Response's text does not match expectation: {responses.calls[0].response.text:!r}"

        assert resp.request.method == expected_method, f"Bitex made request to URL with unexpected method: {resp.request.method}"
        assert resp.json() == expected_json, f"Returned JSON does not match expected JSON for url {expected_url}"


class TestBitexResponse:

    @pytest.mark.parametrize(
        argnames="endpoint, rtype",
        argvalues=[("Ticker", "ticker"), ("Depth", "book"), ("Trades", "trades")],
    )
    @responses.activate
    @patch("bitex_kraken.response.time", return_value="<ts>")
    @patch("bitex_kraken.response.uuid.uuid4", return_value="<uid>")
    def test_triples_method_returns_expected_format(self, mock_time, mock_uid, endpoint, rtype):
        with open(f"tests/data/{rtype}.json") as f:
            responses.add(responses.GET, f"https://api.kraken.com/0/public/{endpoint}?pair=xbtusd", json=json.load(f))

        with open(f"tests/data/{rtype}-triples.json") as f:
            expected = json.load(f)

        session = BitexSession()
        resp = session.get(f"kraken://btcusd/{rtype}")

        actual = resp.triples()

        assert (row in actual for row in expected), "Not all expected rows were found in output!"

    @pytest.mark.parametrize(
        argnames="endpoint, rtype",
        argvalues=[("Ticker", "ticker"), ("Depth", "book"), ("Trades", "trades")],
    )
    @responses.activate
    @patch("bitex_kraken.response.time", return_value="<ts>")
    @patch("bitex_kraken.response.uuid.uuid4", return_value="<uid>")
    def test_key_value_dict_method_returns_expected_format(self, mock_time, mock_uid, endpoint, rtype):
        with open(f"tests/data/{rtype}.json") as f:
            responses.add(responses.GET, f"https://api.kraken.com/0/public/{endpoint}?pair=xbtusd", json=json.load(f))

        with open(f"tests/data/{rtype}-kv.json") as f:
            expected = json.load(f)

        session = BitexSession()
        resp = session.get(f"kraken://btcusd/{rtype}")

        actual = resp.key_value_dict()

        assert (d in actual for d in expected), "Not all expected rows were found in output!"
