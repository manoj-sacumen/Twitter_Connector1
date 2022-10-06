"""Authentication module acts as the facilitator to access the key info related to accessing the API."""
import os

from dotenv import load_dotenv

from src.log import log
from src.std_log import (GET_API_KEY, GET_API_SECRET_KEY, GET_API_TOKEN,
                         LOAD_ENV_FILE)


class Authentications:
    """Authentications class will help in accessing, maintaining the key's and tokens related to Authentications."""

    def __init__(self):
        """Initialize Authentications class by loading the env file form project environment."""
        self.load_env_file()

    @staticmethod
    def load_env_file() -> None:
        """Load env variables from env file."""
        log.info(LOAD_ENV_FILE)
        load_dotenv()

    @staticmethod
    def get_api_token() -> str:
        """Get the API token key from env file.

        Returns:
            str: API token key
        """
        log.debug(GET_API_TOKEN)
        return str(os.getenv('API_TOKEN'))

    @staticmethod
    def get_api_key() -> str:
        """Get the API Key from env file.

        Returns:
            str: API Key
        """
        log.debug(GET_API_KEY)
        return str(os.getenv('API_KEY'))

    @staticmethod
    def get_api_secret_key() -> str:
        """Get the API secret key from env file.

        Returns:
            _type_: API secret key
        """
        log.debug(GET_API_SECRET_KEY)
        return str(os.getenv('API_SECRET_KEY'))

    @staticmethod
    def get_token_type() -> str:
        """Get Token Type.

        Returns:
            str: Token Type
        """
        return str(os.getenv('TOKEN_TYPE'))

# if __name__ == '__main__':
#     auth = Authentications()
#     log.debug(auth.get_api_key())
#     log.debug(auth.get_api_token())
#     log.debug(auth.get_api_secret_key())
