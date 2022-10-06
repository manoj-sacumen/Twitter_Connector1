"""test file writer file holds unittest cases for file writer module."""

import json
import os
import sys

import pytest

from src.file_writer import FileWriter
from tests.utility import (create_response_obj, get_test_input_data,
                           get_test_output_data)

sys.path.append("./src")


def check_for_initialized_state(file_writer, data):
    """Act as helper function to check initialized state of class."""
    assert file_writer.text_content == data.text_content
    assert file_writer.bytes_content == data.bytes_content
    assert file_writer.mode == data.mode
    assert file_writer.data == data.data
    assert file_writer.content_type == data.content_type
    assert file_writer.file_path == data.file_path
    assert file_writer.response == data.response


def test_file_writer_initialization():
    """Check for initialized state of the file_writer class."""
    data = get_test_input_data(func_name='initialized_state')
    file_writer = FileWriter()
    check_for_initialized_state(file_writer, data)


def test_sett():
    """Check for set functionality of file_writer."""
    data = get_test_input_data()
    file_writer = FileWriter()
    file_writer.sett(data.file_path, data.content_type, data.response)

    assert file_writer.file_path == data.file_path
    assert file_writer.content_type == data.content_type
    assert file_writer.response == data.response


def test_reset():
    """Check for reset functionality of file_writer."""
    data = get_test_input_data(func_name='initialized_state')
    file_writer = FileWriter()
    file_writer.sett(filepath='./test/test.json', content_type='json', response='')
    file_writer.reset()
    check_for_initialized_state(file_writer, data)


def test_path_exists_positive():
    """Check for path exists utility function positive case."""
    path = get_test_input_data().path
    file_writer = FileWriter()
    assert file_writer.path_exists(path)


def test_path_exists_negative():
    """Check for path exists utility function negative case."""
    path = get_test_input_data().path
    file_writer = FileWriter()
    assert not file_writer.path_exists(path)


def test_get_parent_path():
    """Check for functionality of getting parent directory path."""
    input_path = get_test_input_data().path
    output_path = get_test_output_data().path
    file_writer = FileWriter()
    assert output_path == file_writer.get_parent_path(input_path)


def test_create_dirs():
    """Check for functionality of creating directory with non-existing path."""
    path = get_test_input_data().path
    file_writer = FileWriter()
    file_writer.create_dirs(path)
    assert os.path.exists(path)


def test_create_dirs_already_exists():
    """Check for functionality of creating directory with existing path."""
    path = get_test_input_data().path
    os.makedirs(path, exist_ok=True)
    file_writer = FileWriter()
    file_writer.create_dirs(path)
    assert os.path.exists(path)
    os.rmdir(path)
    os.rmdir(os.path.dirname(path))


def test_load_response_text_in_json():
    """Check for functionality of loading response text to json."""
    # setup
    input_path = get_test_input_data().path
    expected_path = get_test_output_data().path
    response_obj = create_response_obj(text_data=open(input_path).read())
    file_writer = FileWriter()
    file_writer.response = response_obj
    # test function
    data_loaded = file_writer.load_response_text_in_json()
    # asserting
    expected_data = json.loads(open(expected_path).read())
    assert data_loaded == expected_data


def test_load_response_text_in_json2():
    """Load of response text negative scenario which raises JSONDecodeError."""
    # setup
    response_obj = create_response_obj(text_data='{"data":"abcd"}{}')
    file_writer = FileWriter()
    file_writer.response = response_obj
    # test function
    data_loaded = file_writer.load_response_text_in_json()
    # asserting
    assert data_loaded == {}


def test_load_response_text_in_json3():
    """Load response text data without key data."""
    # setup
    response_obj = create_response_obj(text_data='{"meta":"only_meta_data"}')
    file_writer = FileWriter()
    file_writer.response = response_obj
    # test function
    data_loaded = file_writer.load_response_text_in_json()
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
    """Test functionality of selection of data from response object based on parameters."""
    file_writer = FileWriter()
    file_writer.response = create_response_obj(text_data='{}')
    file_writer.content_type = content_type
    assert expected_content == file_writer.get_data_to_write()


def test_check_for_file_dir_existence():
    """Test for parent dir of file existence else creating dir."""
    path = get_test_input_data().path
    file_writer = FileWriter()
    file_writer.file_path = path
    file_writer.check_for_file_dir_existence()
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
    """Test for selecting mode based on the parameters passed."""
    file_writer = FileWriter()
    file_writer.file_path = file_path
    file_writer.content_type = content_type
    assert expected_mode == file_writer.select_mode()


def test_write_json_file():
    """Test for functionality which writes json file."""
    input_data = get_test_input_data()
    file_writer = FileWriter()
    file_writer.file_path = input_data.file_path
    file_writer.mode = input_data.mode
    file_writer.data = json.loads(open(input_data.data).read())
    # function call
    file_writer.write_json_file()
    # assert testing
    written_data = json.loads(open(file_writer.file_path).read())
    assert written_data['meta']['next_token'] == file_writer.data['meta']['next_token']
    # tear up delete
    os.remove(file_writer.file_path)


def test_write_response_to_file():
    """Test for functionality which handles all steps in writing response to a file."""
    input_data = get_test_input_data()
    file_writer = FileWriter()
    response = create_response_obj(text_data='{"meta":"only_meta_data"}')
    file_writer.write_response_to_file(filepath=input_data.file_path,
                                       response=response,
                                       content_type=input_data.content_type)
    expected_data = json.loads(open(input_data.file_path).read())
    assert expected_data['meta'] == 'only_meta_data'
