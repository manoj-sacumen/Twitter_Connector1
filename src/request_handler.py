"""Request handler provides access to request module functionality."""

from sac_requests.constants.general import BEARER_TOKEN, HTTPS
from sac_requests.context.config import HttpConfig
from sac_requests.context.headers import HttpHeaders
from sac_requests.context.request import (HttpRequest, HttpRequestError,
                                          Response)
from sac_requests.context.url import HttpURL


class RequestHandler:
    """RequestHandler class will create http request handler."""

    """RequestHandler will set up the config for making http request."""

    def __init__(self, headers: dict, host: str, auth_type: str = BEARER_TOKEN) -> None:
        """Initialize Http header,config,url for request handling."""
        self.auth_type = auth_type
        self.base_host = host
        self.headers = headers
        self.http_headers = HttpHeaders(headers=self.headers)
        self.http_url = HttpURL(host=self.base_host, protocol=HTTPS)
        self.http_config = self.create_config()

        self.http_request = HttpRequest(headers=self.http_headers, url=self.http_url,
                                        config=self.http_config)

    def create_config(self) -> HttpConfig:
        """Create http config object which will modify behaviour of http request object."""
        return HttpConfig(
            timeout=20,
            retry_interval=1,
            status_force_list=[429, 500, 502, 503, 504, 400],
            max_retry=3,
            auth_type=self.auth_type)

    def send_get_request(self, endpoint) -> Response:
        """Send request to the pre-set url and config with given end points."""
        response = Response()
        try:
            response = self.http_request.get(endpoint=endpoint, headers=self.headers, data={})
        except HttpRequestError as err:
            response.status_code = err.errcode
        return response
