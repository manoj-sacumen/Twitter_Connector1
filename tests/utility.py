"""utility file holds common help functions which will be used in test cases."""
import os
import sys

import requests
import requests_mock

from tests.test_data.test_data import (test_data_collector,
                                       test_data_file_writer)

t_data = {'test_collector': test_data_collector,
          'test_file_writer': test_data_file_writer}


def get_test_input_data(func_name=''):
    """Get the input data for test cases from test_data file."""
    code = sys._getframe(1).f_code
    file_name = os.path.basename(code.co_filename).strip('.py')
    if not func_name:
        func_name = code.co_name
    return t_data[file_name][func_name]['input']


def get_test_output_data(func_name=''):
    """Get the output data for test cases from test_data file."""
    code = sys._getframe(1).f_code
    file_name = os.path.basename(code.co_filename).strip('.py')
    if not func_name:
        func_name = code.co_name
    return t_data[file_name][func_name]['output']


def create_response_obj(text_data='', status_code=200):
    """Create dummy response object with given parameters."""
    with requests_mock.Mocker() as mock:
        mock.get('http://mock_path', text=text_data, status_code=status_code)
        return requests.get('http://mock_path')
