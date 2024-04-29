import logging
import logging.config
import os

import yaml
from config import configs


class OCRLogger:
    def __init__(self, conf_file: str = configs.DIR_CONFIG.LOG_CONFIG_FILE) -> None:
        """
        Initializes an instance of OCRLogger.

        Args:
            config_file (str): Path to the log configuration file. Defaults to LOG_CONFIG_FILE.
        """
        dirname = os.path.dirname(__file__)
        with open(conf_file) as config_file:
            config = yaml.safe_load(config_file)
        config['handlers']['file']['filename'] = os.path.join(dirname, configs.DIR_CONFIG.LOG_FILE)
        with open(conf_file, 'w') as config_file:
            yaml.dump(config, config_file)

        self.logger = logging.config.dictConfig(config)
        self.logger = logging.getLogger('xero_logger')

    def log_debug(self, message: str) -> None:
        """
        Logs a debug message.

        Args:
            message (str): The message to log.
        """
        self.logger.debug(message)

    def log_info(self, message: str) -> None:
        """
        Logs an info message.

        Args:
            message (str): The message to log.
        """
        self.logger.info(message)

    def log_warning(self, message: str) -> None:
        """
        Logs a warning message.

        Args:
            message (str): The message to log.
        """
        self.logger.warning(message)

    def log_error(self, message: str) -> None:
        """
        Logs an error message.

        Args:
            message (str): The message to log.
        """
        self.logger.error(message)

    def log_critical(self, message: str) -> None:
        """
        Logs a critical message.

        Args:
            message (str): The message to log.
        """
        self.logger.critical(message)



logger = OCRLogger()
