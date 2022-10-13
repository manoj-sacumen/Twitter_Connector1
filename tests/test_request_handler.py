"""Tests request handler module functionality."""
import json

from sac_requests.context.request import Response

from src.collector import Collector
from tests.utility import get_test_input_data


def test_send_get_request():
    """Test functionality which sends request to given endpoint."""
    input_data = get_test_input_data()
    end_point = input_data.end_point
    col = Collector()
    response = col.request_handel.send_get_request(endpoint=end_point)
    assert isinstance(response, Response)
    if col.response.status_code == 200:
        assert input_data.query in col.response.text
        json_data = json.loads(col.response.text)
        assert json_data['meta']['result_count'] <= input_data.max_results
    else:
        print('Request Failed in test_send_request,', col.response)
