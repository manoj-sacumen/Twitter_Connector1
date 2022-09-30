# Standard library's
import os
# third party library's
from dotenv import load_dotenv
# Local library's
from Twitter_connector.log import log
from Twitter_connector.std_log import (
    GETAPIKEY, GETAPISECRETKEY, GETAPITOKEN, LOADENVFILE)


class Authentications:
    """
    Authentications class will help in accessing and maintaining
    the key's and tokens related to Authentications.
    Will do getter and setter functionalities of keys and tokens
    """

    def __init__(self):
        self.load_env_file()

    @staticmethod
    def load_env_file():
        """
        Loading env variables from env file
        """
        log.info(LOADENVFILE)
        load_dotenv()

    @staticmethod
    def get_api_token() -> str:
        """ Gets the API token key from env file
        Returns:
            str: API token key
        """
        log.debug(GETAPITOKEN)
        return os.getenv('API_TOKEN')

    @staticmethod
    def get_api_key() -> str:
        """ Gets the API Key from env file
        Returns:
            str: API Key
        """
        log.debug(GETAPIKEY)
        return os.getenv('API_KEY')

    @staticmethod
    def get_api_secret_key() -> str:
        """ Gets the API secret key from env file

        Returns:
            _type_: API secret key
        """
        log.debug(GETAPISECRETKEY)
        return os.getenv('API_SECRET_KEY')

    # @staticmethod
    # def set_api_token(token: str) -> None:
    #     """ Sets the API token key to env file
    #     Args:
    #         token (str): API token key
    #     """
    #     os.environ['API_TOKEN'] = token
    #     log.debug(SETAPITOKEN)

    # @staticmethod
    # def set_api_key(key: str) -> None:
    #     """ Sets the API key to env file
    #     Args:
    #         key (str): API key
    #     """
    #     os.environ['API_KEY'] = key
    #     log.debug(SETAPIKEY)

    # @staticmethod
    # def set_api_secret_key(key: str) -> None:
    #     """ Sets the API secret key to env file
    #     Args:
    #         key (str): API secret key
    #     """
    #     os.environ['API_SECRET_KEY'] = key
    #     log.debug(SETAPISECRETKEY)

    @staticmethod
    def get_token_type() -> str:
        """ Get Token Type
        Returns:
            str: Token Type
        """
        return os.getenv('TOKEN_TYPE')


# if __name__ == '__main__':
#     auth = Authentications()
#     log.debug(auth.get_api_key())
#     log.debug(auth.get_api_token())
#     log.debug(auth.get_api_secret_key())
