# standard library's
import pytest
import json
import sys
import os
# third party library's
import requests_mock
import requests
# local modules
from .test_data.test_data import test_data_file_writer as t_data
from Twitter_connector.file_writer import FileWriter

sys.path.append("./Twitter_connector")


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


def check_for_initialized_state(fw, data):
    assert fw.text_content == data.text_content
    assert fw.bytes_content == data.bytes_content
    assert fw.mode == data.mode
    assert fw.data == data.data
    assert fw.content_type == data.content_type
    assert fw.file_path == data.file_path
    assert fw.response == data.response


def test_file_writer_initialization():
    data = get_test_input_data(func_name='initialized_state')
    fw = FileWriter()
    check_for_initialized_state(fw, data)


def test_sett():
    data = get_test_input_data()
    fw = FileWriter()
    fw.sett(data.file_path, data.content_type, data.response)

    assert fw.file_path == data.file_path
    assert fw.content_type == data.content_type
    assert fw.response == data.response


def test_reset():
    data = get_test_input_data(func_name='initialized_state')
    fw = FileWriter()
    fw.sett(filepath='./test/test.json', content_type='json', response='')
    fw.reset()
    check_for_initialized_state(fw, data)


def test_path_exists_positive():
    path = get_test_input_data().path
    fw = FileWriter()
    assert fw.path_exists(path)


def test_path_exists_negative():
    path = get_test_input_data().path
    fw = FileWriter()
    assert not fw.path_exists(path)


def test_get_parent_path():
    input_path = get_test_input_data().path
    output_path = get_test_output_data().path
    fw = FileWriter()
    assert output_path == fw.get_parent_path(input_path)


def test_create_dirs():
    path = get_test_input_data().path
    fw = FileWriter()
    fw.create_dirs(path)
    assert os.path.exists(path)


def test_create_dirs_already_exists():
    path = get_test_input_data().path
    os.makedirs(path, exist_ok=True)
    fw = FileWriter()
    fw.create_dirs(path)
    assert os.path.exists(path)
    try:
        os.rmdir(path)
        os.rmdir(os.path.dirname(path))
    except Exception as e:
        print(f'Exception in test_create_dirs_already_exists in deleting dir', e)


def test_load_response_text_in_json():
    """ Normal Behaviour"""
    # setup
    input_path = get_test_input_data().path
    expected_path = get_test_output_data().path
    response_obj = create_response_obj(text_data=open(input_path).read())
    fw = FileWriter()
    fw.response = response_obj
    # test function
    data_loaded = fw.load_response_text_in_json()
    # asserting
    assert str(data_loaded) == open(expected_path).read()


def test_load_response_text_in_json2():
    """ JSONDecodeError """
    # setup
    response_obj = create_response_obj(text_data='{"data":"abcd"}{}')
    fw = FileWriter()
    fw.response = response_obj
    # test function
    data_loaded = fw.load_response_text_in_json()
    # asserting
    assert data_loaded == {}


def test_load_response_text_in_json3():
    """ input data without data key """
    # setup
    response_obj = create_response_obj(text_data='{"meta":"only_meta_data"}')
    fw = FileWriter()
    fw.response = response_obj
    # test function
    data_loaded = fw.load_response_text_in_json()
    # asserting
    assert data_loaded == {"meta": "only_meta_data"}


@pytest.mark.parametrize("content_type,expected_content",
                         [
                             pytest.param('text', '{}', id='text'),
                             pytest.param('json', {}, id='json'),
                             pytest.param('zip', b'{}', id='bytes')
                         ],
                         )
def test_get_data_to_write(content_type, expected_content):
    fw = FileWriter()
    fw.response = create_response_obj(text_data='{}')
    fw.content_type = content_type
    assert expected_content == fw.get_data_to_write()


def test_check_for_file_dir_existence():
    """check_for_file_dir_existence else creating dir"""
    path = 'tests/test_data/file_dir_existence/temp.log'
    fw = FileWriter()
    fw.file_path = path
    fw.check_for_file_dir_existence()
    dir_path = os.path.dirname(path)
    if os.path.exists(dir_path):
        os.rmdir(dir_path)
    else:
        assert False


@pytest.mark.parametrize("file_path,content_type,expected_mode",
                         [pytest.param(__file__, 'text', 'a', id='existing_text_file'),
                          pytest.param(__file__, 'zip', 'ab',
                                       id='existing_bytes_file'),
                          pytest.param('/dummy/non/existing.py', 'zip',
                                       'wb', id='non_existing_bytes_file'),
                          pytest.param('/dummy/non/existing.py',
                                       'text', 'w', id='non_existing_text_file')
                          ])
def test_select_mode(file_path, content_type, expected_mode):
    fw = FileWriter()
    fw.file_path = file_path
    fw.content_type = content_type
    assert expected_mode == fw.select_mode()


def test_write_json_file():
    input_data = get_test_input_data()
    fw = FileWriter()
    fw.file_path = input_data.file_path
    fw.mode = input_data.mode
    fw.data = json.loads(open(input_data.data).read())
    # function call
    fw.write_json_file()
    # assert testing
    written_data = json.loads(open(fw.file_path).read())
    assert written_data['meta']['next_token'] == fw.data['meta']['next_token']
    # tear up delete
    os.remove(fw.file_path)


def test_write_response_to_file():
    input_data = get_test_input_data()
    fw = FileWriter()
    response = create_response_obj(text_data='{"meta":"only_meta_data"}')
    fw.write_response_to_file(filepath=input_data.file_path,
                              response=response,
                              content_type=input_data.content_type)
    expected_data = json.loads(open(input_data.file_path).read())
    assert expected_data['meta'] == 'only_meta_data'


