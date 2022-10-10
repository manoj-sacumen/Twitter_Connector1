"""Request handler provides access to request module functionality."""
import requests  # type: ignore


def send_request(url: str, method: str, headers: dict, data: dict) -> requests.Response:
    """Make a request for the defined parameters."""
    response = requests.request(method=method, url=url, headers=headers, data=data)
    return response
