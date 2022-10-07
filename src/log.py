"""Log module will provide logging functionalities to the project as per configuration done in log config."""
# standard library's
import logging

# local library's
import src.log_config as log_config
from src.std_log import LOG_SETUP_DONE

logging.basicConfig(filename=log_config.FILE_NAME,
                    level=log_config.LOG_LEVEL,
                    format=log_config.LOG_FORMAT,
                    datefmt=log_config.DATE_FORMAT)

log = logging.getLogger(__name__)
log.info(LOG_SETUP_DONE)
