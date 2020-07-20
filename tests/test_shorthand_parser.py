from abc import ABC, abstractmethod
import pytest

from bitex.session import BitexSession
from bitex.constants.testing import BITEX_SHORTHAND_ENDPOINTS
from bitex.plugins import PLUGINS

from bitex_kraken.constants import KRAKEN_API, ENDPOINT_MAPPING


@pytest.mark.parametrize(
    "given, expected",
    argvalues=[
        (f"kraken://xbtusd/{key}", f"{KRAKEN_API}/public/{value}?pair=XXBTZUSD")
        for key, value in ENDPOINT_MAPPING.items()
        if key in BITEX_SHORTHAND_ENDPOINTS["public"]
    ],
    ids=BITEX_SHORTHAND_ENDPOINTS["public"],
)
def test_shorthand_parser_for_public_endpoints(given, expected):
    assert BitexSession().


class TestShorthandParser(ABC):
    @abstractmethod
    def setup_tests(self, exchange_name, class_instance, http_method_mapping, http_exc_mapping, valid_pair):
        """Configure the variables required for this class' tests.

        :param obj class_instance: Instance of the class under test.
        :param dict http_method_mapping:
            A regex-to-http-method mapping. The regex is used to determine what
            method should be used when making requests. It's matched against the
            **bitex shorthand**, not the final url.
        :param dict http_exc_mapping:
            A (status-code, key, err_msg)-to-raides-exception mapping. If error
            messages are not required to raise an exception, `key` may be None.
        :param str valid_pair:
            A valid, supported asset pair to make requests with.
        """
        self.exchange_name = exchange_name
        self.test_instance = class_instance
        self.http_method_mapping = http_method_mapping
        self.http_exc_mapping = http_exc_mapping
        self.valid_pair, self.invalid_pair = valid_pair, valid_pair + "_invalid"

    def make_shorthand_url(self, endpoint, action=None):
        url = f"{self.exchange_name}://{self.valid_pair}/{endpoint}"
        if action:
            return f"{url}/{action}"
        return url

    def test_invalid_pair_raises_unknown_pair_exception(self):
        """Ensure that we check supplied pairs before making requests against
        the list of known pairs.

        The following assertions are made:
        -   A :mod:`bitex` exception is raised
        -   No request was made via :func:`requests.request`
        """

    def test_unknown_parameter_raises_invalid_args_exception(self):
        """Ensure that 400 Bad Request responses due to invalid parameters
        raise the appropriate :mod:`bitex` exception."""

    def test_return_value_is_a_valid_url_if_requests_needs_no_body(self):
        """Requests to endpoints which require the GET http method should not
        have a request body, and any parameters required by such a request
        should be urlencoded into the request URL. Assert this is the case
        for the specific endpoints.
        """

    def test_return_value_is_a_url_dict_tuple_if_requests_needs_a_body(self):
        """Requests to endpoints which require the POST http method typically
        need the request parameters supplied via the body. Assert that shorthands
        requesting to such API endpoints return a tuple of type (url, dict).
        """
