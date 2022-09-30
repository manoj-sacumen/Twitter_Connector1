# standard library's
import logging
# local library's
import Twitter_connector.log_config as log_config
from Twitter_connector.std_log import LOGSETUPDONE

logging.basicConfig(filename=log_config.file_name,
                    level=log_config.log_level,
                    format=log_config.log_format,
                    datefmt=log_config.date_format)

log = logging.getLogger(__name__)
log.info(LOGSETUPDONE)


