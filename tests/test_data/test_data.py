# standard library's
from requests import Response
import sys
import os
# third party library's
from box import Box
# local modules
from Twitter_connector.std_log import TEXT_CONTENT, BYTES_CONTENT


sys.path.append("./Twitter_connector")

t_data = {
    'test_sett': {
        'input': {'file_path': 'test_path/test_file.json',
                  'content_type': 'json',
                  'response': Response()},
        'output': {}
    },
    'initialized_state': {
        'input': {'text_content': TEXT_CONTENT,
                  'bytes_content': BYTES_CONTENT,
                  'mode': 'w',
                  'data': {},
                  'content_type': '',
                  'file_path': '',
                  'response': None
                  },
        'output': {}
    },
    'test_path_exists_positive': {
        'input': {'path': os.path.abspath(__file__)},
        'output': {}
    },
    'test_path_exists_negative': {
        'input': {'path': './Non/existing/path.json'},
        'output': {}
    },
    'test_get_parent_path': {
        'input': {'path': os.path.abspath(__file__)},
        'output': {'path': os.path.dirname(__file__)}
    },
    'test_create_dirs': {
        'input': {'path': f'{os.path.dirname(__file__)}/temp1'},
        'output': {}
    },
    'test_create_dirs_already_exists': {
        'input': {'path': f'{os.path.dirname(__file__)}/temp1/temp2'},
        'output': {}
    },
    'test_load_response_text_in_json1': {
        'input': {'path': open('tests/test_data/load_response_text_in_json/1/input_data.json').read},
        'output': {'path': open('tests/test_data/load_response_text_in_json/1/expected_data.txt').read}
    },
    'test_write_json_file':{
        'input': {'data': 'tests/test_data/write_json_file/input_json_data.json',
                  'file_path': 'tests/test_data/write_json_file/output_json_data.json',
                  'mode': 'w'},
        'output': {}
    },
    'test_write_response_to_file':{
        'input': {'file_path': 'tests/test_data/write_json_file/output_json_data.json',
                  'content_type': 'json'},
        'output': {}
    }






}

t_data=Box(t_data)