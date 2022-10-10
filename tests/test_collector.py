"""test collection file holds unittest cases for collector module."""
import json
import os

import pytest

from src.api_config import STORE_DIR
from src.collector import Collector
from tests.utility import (create_response_obj, get_test_input_data,
                           get_test_output_data)


def test_generate_querystring():
    """Test to check generation of query string from given parameters."""
    params = get_test_input_data()
    col = Collector()
    col.generate_querystring(params)
    assert col.querystring == get_test_output_data()


def test_create_url():
    """Test to check creation of url from given parts of url."""
    input_data = get_test_input_data()
    col = Collector()
    col.url_path = input_data.url_path
    col.querystring = input_data.querystring
    col.create_url()
    assert col.url == get_test_output_data().url


def test_get_auth_token():
    """Test to check functionality of getting authentication token from Env."""
    input_data = get_test_input_data()
    output_data = get_test_output_data()
    os.environ['TOKEN_TYPE'] = input_data.test_token
    os.environ['API_TOKEN'] = input_data.test_api_token
    col = Collector()
    assert col.get_auth_token() == output_data.auth_token
    # tear up
    del os.environ['TOKEN_TYPE']
    del os.environ['API_TOKEN']


@pytest.mark.parametrize('status_code,fn_prefix',
                         [
                             pytest.param(200, 'success_', id='success'),
                             pytest.param(400, 'failure_', id='failure'),
                             pytest.param(100, 'undefined_', id='undefined')
                         ],
                         )
def test_handles_response(status_code, fn_prefix):
    """Test functionality which handles response for sent request."""
    output_data = get_test_output_data()[status_code]
    input_data = get_test_input_data()
    col = Collector()
    col.response = create_response_obj(text_data=input_data.text_data,
                                       status_code=status_code)
    col.current_key = f'test_handles_response_{status_code}'
    col.handles_response()
    # success file written with data content
    file_path = f'{STORE_DIR}/{fn_prefix}{col.current_key}.json'
    if os.path.exists(file_path):
        content = open(file_path).read()
        # Note: when file is appended, content will not be in proper format so raises error
        data = json.loads(content)
        os.remove(file_path)
        assert output_data.text_data == data
    else:
        assert False
    # next token data taken
    assert col.next_token == output_data.next_token


def test_set_url_path_by_user_id():
    """Test selecting of url path for requests done based on user id."""
    input_data = get_test_input_data()
    output_data = get_test_output_data()
    col = Collector()
    col.set_url_path(val=input_data.param)
    assert col.url_path == output_data.url_path


def test_set_url_path_recent_tweets():
    """Test selecting of url path for requests done based on recent tweets."""
    input_data = get_test_input_data()
    output_data = get_test_output_data()
    col = Collector()
    col.set_url_path(val=input_data.param)
    assert col.url_path == output_data.url_path


def test_check_for_next_page_data_with_next_token():
    """Test functionality which parse response to get next token for valid scenario."""
    input_data = get_test_input_data()
    output_data = get_test_output_data()
    col = Collector()
    col.response = create_response_obj(text_data=input_data.text_data,
                                       status_code=200)
    col.check_for_next_page_data()
    assert col.next_token == output_data.next_token


def test_check_for_next_page_data_without_next_token():
    """Test functionality which parse response to get next token for in-valid scenario."""
    input_data = get_test_input_data()
    output_data = get_test_output_data()
    col = Collector()
    col.response = create_response_obj(text_data=input_data.text_data,
                                       status_code=200)
    col.check_for_next_page_data()
    assert col.next_token == output_data.next_token


def test_get_tweets():
    """Test get tweets functionality which acts as main actuator."""
    input_data = get_test_input_data()
    output_data = get_test_output_data()
    col = Collector()
    col.params = input_data.params
    col.get_tweets()
    assert col.response.status_code == output_data.status_code
    file_path = output_data.file_path
    if os.path.exists(file_path):
        content = open(file_path).read()
        for ids in output_data.expected_msgs_id:
            if ids not in content:
                assert False
    else:
        assert False
    assert col.next_token == output_data.next_token


def test_create_query_params_today_tweets():
    """Test for updating user given input to template parameter set."""
    input_data = get_test_input_data()
    expected_data = get_test_output_data()
    import datetime
    now = datetime.datetime.now
    today = now().strftime("%Y-%m-%dT00:00:00Z")
    tomorrow = (now() + datetime.timedelta(1)).strftime("%Y-%m-%dT00:00:00Z")
    col = Collector()
    col.create_query_params(input_data.params, name=input_data.name)
    key = 'Data_on_' + str(input_data.name)
    value = col.params[key]
    query_params = value['query_params']
    assert query_params['start_time'] == today
    assert query_params['end_time'] == tomorrow
    assert query_params['query'] == expected_data.query_params.query
    assert query_params['max_results'] == expected_data.query_params.max_results


def test_create_query_params_tweets_by_datetime():
    """Test for updating user given input to template parameter set."""
    input_data = get_test_input_data()
    expected_data = get_test_output_data()
    col = Collector()
    col.create_query_params(input_data.params, name=input_data.name)
    key = 'Data_on_' + str(input_data.name)
    assert col.params[key] == expected_data


def test_create_query_params_user_tweets():
    """Test for updating user given input to template parameter set."""
    input_data = get_test_input_data()
    expected_data = get_test_output_data()
    col = Collector()
    col.create_query_params(input_data.params, name=input_data.name)
    key = 'Data_on_' + str(input_data.name)
    assert col.params[key] == expected_data
    print()
