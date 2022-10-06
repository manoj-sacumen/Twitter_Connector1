"""test_authentication file holds unit test cases for Authentication module."""
# standard library's
import os
import sys

from src.authentications import Authentications

# needs better solution for relative import issue.
sys.path.append("./src")
auth = Authentications()


def test_get_api_token():
    """Test function to check functionality of getting API token from Env variables."""
    assert auth.get_api_token() == os.environ['API_TOKEN']


def test_get_api_key():
    """Test function to check functionality of getting API key from Env variables."""
    assert auth.get_api_key() == os.environ['API_KEY']


def test_get_api_secret_key():
    """Test function to check functionality of getting API secret key from Env variables."""
    assert auth.get_api_secret_key() == os.environ['API_SECRET_KEY']


def test_get_token_type():
    """Test function to check functionality of getting API token type from Env variables."""
    assert auth.get_token_type() == os.environ['TOKEN_TYPE']


def test_load_env_file():
    """Test function to check functionality of getting API token from Env variables."""
    # https://adamj.eu/tech/2020/10/13/how-to-mock-environment-variables-with-pytest/
    # print(os.environ['TOKEN_TYPE'])
    auth.load_env_file()
    # still need to figure which method to test

# set functionalities test cases will be written if auto key generation is possible.
