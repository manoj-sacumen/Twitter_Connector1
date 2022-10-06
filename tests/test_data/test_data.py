"""Test data file holds the input and output data required to run test cases."""
import os
import sys

from box import Box
from requests import Response

from src.api_config import API_URL
from src.std_log import BYTES_CONTENT, TEXT_CONTENT

sys.path.append("./src")

test_data_file_writer = {
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
    'test_load_response_text_in_json': {
        'input': {'path': 'tests/test_data/load_response_text_in_json/input_data.json'},
        'output': {'path': 'tests/test_data/load_response_text_in_json/expected_data.txt'}
    },
    'test_write_json_file': {
        'input': {'data': 'tests/test_data/write_json_file/input_json_data.json',
                  'file_path': 'tests/test_data/write_json_file/output_json_data.json',
                  'mode': 'w'},
        'output': {}
    },
    'test_write_response_to_file': {
        'input': {'file_path': 'tests/test_data/write_json_file/output_json_data.json',
                  'content_type': 'json'},
        'output': {},
    },
    'test_check_for_file_dir_existence': {
        'input': {'path': 'tests/test_data/file_dir_existence/temp.log'},
        'output': {}
    }

}

test_data_file_writer = Box(test_data_file_writer)
test_data_collector = {
    'test_generate_querystring': {
        'input': {'query': 'India',
                  'start_time': '2022-09-24T00:00:00Z',
                  'end_time': '2022-09-24T01:00:00Z',
                  'max_results': 10},
        'output': 'query=India&start_time=2022-09-24T00:00:00Z&end_time=2022-09-24T01:00:00Z&max_results=10'
    },
    'test_create_url': {
        'input': {'url_path': '/2/tweets/search/recent',
                  'querystring': 'query=india&start_time=2022-09-29T00:00:00Z&end_time=2022-09-29T01:00:00Z'},
        'output': {
            'url': f'{API_URL}/2/tweets/search/recent?query=india&start_time=2022-09-29T00:00:00Z&end_time=2022-09-29T01:00:00Z'}
    },
    'test_get_auth_token': {
        'input': {'test_token': 'test_token',
                  'test_api_token': 'test_api_token'},
        'output': {'auth_token': 'test_token test_api_token'}
    },
    'test_send_request': {
        'input': {'method': 'GET',
                  'url': f'{API_URL}/2/tweets/search/recent?query=India&max_results=10',
                  'query': 'India',
                  'max_results': 10},
        'output': {}
    },
    'test_handles_response': {
        'input': {'text_data': '{"data":{"text":"abcdefg"},"meta":{"next_token":"123456789"}}',
                  },
        'output': {200: {'text_data': {"text": "abcdefg"}, 'next_token': '123456789'},
                   400: {'text_data': {"text": "abcdefg"}, 'next_token': ''},
                   100: {'text_data': {"text": "abcdefg"}, 'next_token': ''}
                   }

    },
    'test_set_url_path_by_user_id': {
        'input': {'param': {'search_type': 'By_User_ID',
                            'user_id': 54829997,
                            'path': '/2/users'}
                  },
        'output': {'url_path': '/2/users/54829997/tweets'}
    },
    'test_set_url_path_recent_tweets': {
        'input': {'param': {'search_type': 'Recent_tweets',
                            'method': 'GET',
                            'path': '/2/tweets/search/recent'}
                  },
        'output': {'url_path': '/2/tweets/search/recent'}
    },
    'test_check_for_next_page_data_with_next_token': {
        'input': {'text_data': """{"meta": {"newest_id": "1575289156820815872",
                                         "oldest_id": "1575287731236007936",
                                         "result_count": 10,
                                         "next_token": "b26v89c19zqg8o3fpzblrquj0fu4kt8gvruk1m3x2ctj1"}
                                }""",
                  },
        'output': {'next_token': "b26v89c19zqg8o3fpzblrquj0fu4kt8gvruk1m3x2ctj1"}
    },
    'test_check_for_next_page_data_without_next_token': {
        'input': {'text_data': """{"meta": {"newest_id": "1575289156820815872",
                                         "oldest_id": "1575287731236007936",
                                         "result_count": 10,
                                         "token": "b26v89c19zqg8o3fpzblrquj0fu4kt8gvruk1m3x2ctj1"}
                                }"""
                  },
        'output': {'next_token': ""}
    },
    'test_get_tweets': {
        'input': {'params': {'Tweets_by_user_id_test': {'method': 'GET',
                                                        'search_type': 'By_User_ID',
                                                        'user_id': 1572527925186134016,
                                                        'path': '/2/users',
                                                        'query_params': {'max_results': 5,
                                                                         'user.fields': 'created_at,id,name,username',
                                                                         }
                                                        }
                             }
                  },
        'output': {'expected_msgs_id': ['1576837406841442305', '1576837598512676864', '1576837621912772609',
                                        '1576837650786373633', '1576837677357277184', '1576837706495102976'],
                   'next_token': '',
                   'status_code': 200,
                   'file_path': './Response_data/success_Tweets_by_user_id_test.json'}
    }

}
test_data_collector = Box(test_data_collector)
