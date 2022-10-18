"""Log module will provide logging functionalities to the project as per configuration done in log config."""
# standard library's
import locale
import logging

from sac_configurations.input.cfg import CFGConfig

from src.std_log import LOG_SETUP_DONE

locale.setlocale(locale.LC_CTYPE, "en_US.UTF-8")
config_files = ['../config/logging.cfg']
config = CFGConfig()
config.read(config_files)
config_dct = config.to_dict()

LOG_LEVELS = {'CRITICAL': 50,
              'ERROR': 40,
              'WARNING': 30,
              'INFO': 20,
              'DEBUG': 10,
              }
LOGGING = config_dct.get('logging')
LOG_LEVEL = LOG_LEVELS.get(LOGGING.get('log_level'), 'INFO')
file_path = f'../{LOGGING.get("log_file_path", "")}/{LOGGING.get("log_filename", "")}'
logging.basicConfig(filename=file_path,
                    level=LOG_LEVEL,
                    format=LOGGING.get('log_format', ''),
                    datefmt=LOGGING.get('date_format', '')
                    )

log = logging.getLogger(__name__)
log.info(LOG_SETUP_DONE)
