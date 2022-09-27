# standard library's
import logging
# local library's
import log_config
from std_log import LOGSETUPDONE

logging.basicConfig(filename=log_config.file_name,
                    level=log_config.log_level,
                    format=log_config.log_format,
                    datefmt=log_config.date_format)

log = logging.getLogger(__name__)
log.info(LOGSETUPDONE)


