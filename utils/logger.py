"""Logger module with config"""
import logging
from utils.config_parser import config


class Logger:
    """Logger class with loaded handles"""

    log_format = config()["logger"]["log_format"]

    def __init__(self, stream=True, debug=True):
        self.logger = logging.getLogger(__name__)

        if debug:
            self.logger.setLevel('DEBUG')
        else:
            self.logger.setLevel(config()["logger"]["log_level"])

        self.formatter = logging.Formatter(self.log_format)

        self.file_handler = logging.FileHandler(config()["logger"]["log_file"])
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

        if stream:
            self.stream_handler = logging.StreamHandler()
            self.stream_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.stream_handler)

    def debug(self, message):
        """print debug messages"""
        self.logger.debug(message)

    def info(self, message):
        """print info messages"""
        self.logger.info(message)

    def warning(self, message):
        """print warning messages"""
        self.logger.warning(message)

    def error(self, message):
        """print error messages"""
        self.logger.error(message)

    def critical(self, message):
        """print critical messages"""
        self.logger.critical(message)


logger = Logger()
