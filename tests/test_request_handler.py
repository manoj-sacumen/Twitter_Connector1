"""Tests request handler module functionality."""
import json

import requests  # type:ignore

from src.collector import Collector
from src.request_handler import send_request
from tests.utility import get_test_input_data


def test_send_request():
    """Test functionality which sends request to given url."""
    input_data = get_test_input_data()
    method = input_data.method
    url = input_data.url
    col = Collector()
    headers = col.headers
    response = send_request(url=url, method=method, headers=headers, data={})
    assert isinstance(response, requests.Response)
    if col.response.status_code == 200:
        assert input_data.query in col.response.text
        json_data = json.loads(col.response.text)
        assert json_data['meta']['result_count'] <= input_data.max_results
    else:
        print('Request Failed in test_send_request,', col.response)
