# Standard library's
import os
import sys
import json

import pytest
# third party library's
import requests
import requests_mock
from requests import Response
# local library's
from Twitter_connector.collector import Collector
from Twitter_connector.api_config import STORE_DIR
from tests.test_data.test_data import test_data_collector as t_data


def create_response_obj(text_data='', status_code=200):
    with requests_mock.Mocker() as m:
        m.get('http://mock_path', text=text_data,
              status_code=status_code)
        return requests.get('http://mock_path')


def get_test_input_data(func_name=''):
    if not func_name:
        func_name = sys._getframe(1).f_code.co_name
    return t_data[func_name]['input']


def get_test_output_data(func_name=''):
    if not func_name:
        func_name = sys._getframe(1).f_code.co_name
    return t_data[func_name]['output']


def test_collector():
    # don't know what to test
    c = Collector()


def test_generate_querystring():
    params = get_test_input_data()
    c = Collector()
    c.generate_querystring(params)
    assert c.querystring == get_test_output_data()


def test_create_url():
    input_data = get_test_input_data()
    c = Collector()
    c.url_path = input_data.url_path
    c.querystring = input_data.querystring
    c.create_url()
    assert c.url == get_test_output_data().url


def test_get_auth_token():
    input_data = get_test_input_data()
    output_data = get_test_output_data()
    os.environ['TOKEN_TYPE'] = input_data.test_token
    os.environ['API_TOKEN'] = input_data.test_api_token
    c = Collector()
    assert c.get_auth_token() == output_data.auth_token
    # tear up
    del os.environ['TOKEN_TYPE']
    del os.environ['API_TOKEN']


def test_make_request():
    input_data = get_test_input_data()
    c = Collector()
    c.method = input_data.method
    c.url = input_data.url
    c.make_request()
    assert isinstance(c.response, Response)
    if c.response.status_code == 200:
        assert input_data.query in c.response.text
        json_data = json.loads(c.response.text)
        assert json_data['meta']['result_count'] <= input_data.max_results
    else:
        print('Request Failed in test_make_request,', c.response)


@pytest.mark.parametrize('status_code,fn_prefix',
                         [
                             pytest.param(200, 'success_', id='success'),
                             pytest.param(400, 'failure_', id='failure'),
                             pytest.param(100, 'undefined_', id='undefined')
                         ],
                         )
def test_handles_response(status_code, fn_prefix):
    output_data = get_test_output_data()[status_code]
    input_data = get_test_input_data()
    c = Collector()
    c.response = create_response_obj(text_data=input_data.text_data,
                                     status_code=status_code)
    c.current_key = f'test_handles_response_{status_code}'
    c.handles_response()
    # success file written with data content
    file_path = f'{STORE_DIR}/{fn_prefix}{c.current_key}.json'
    if os.path.exists(file_path):
        content = open(file_path).read()
        # Note: when file is appended, content will not be in proper format so raises error
        data = json.loads(content)
        os.remove(file_path)
        assert output_data.text_data == data
    else:
        assert False
    # next token data taken
    assert c.next_token == output_data.next_token


def test_set_url_path_By_User_ID():
    input_data = get_test_input_data()
    output_data = get_test_output_data()
    c = Collector()
    c.set_url_path(val=input_data.param)
    assert c.url_path == output_data.url_path


def test_set_url_path_Recent_tweets():
    input_data = get_test_input_data()
    output_data = get_test_output_data()
    c = Collector()
    c.set_url_path(val=input_data.param)
    assert c.url_path == output_data.url_path


def test_check_for_next_page_data_with_next_token():
    input_data = get_test_input_data()
    output_data = get_test_output_data()
    c =Collector()
    c.response = create_response_obj(text_data=input_data.text_data,
                                     status_code=200)
    c.check_for_next_page_data()
    assert c.next_token == output_data.next_token


def test_check_for_next_page_data_without_next_token():
    input_data = get_test_input_data()
    output_data = get_test_output_data()
    c = Collector()
    c.response = create_response_obj(text_data=input_data.text_data,
                                     status_code=200)
    c.check_for_next_page_data()
    assert c.next_token == output_data.next_token


def test_get_tweets():
    input_data = get_test_input_data()
    output_data = get_test_output_data()
    c= Collector()
    c.get_tweets(input_data.params)
    print()
    assert c.response.status_code == output_data.status_code
    file_path = output_data.file_path
    if os.path.exists(file_path):
        content = open(file_path).read()
        for ids in output_data.expected_msgs_id:
            if ids not in content:
                assert False
    else:
        assert False
    assert c.next_token == output_data.next_token



