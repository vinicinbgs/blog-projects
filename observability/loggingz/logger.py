"""  
A logger class that supports configuration flexibility and environment variable
"""

import json
import logging
import logging.config
import os
import sys


class Logger:
    """
    A logger class that supports configuration flexibility and environment variable
    overrides for the log level.

    This class allows you to define a logger with a name and optionally load a
    configuration file or use a basic configuration. The LOG_LEVEL from the
    configuration file can be overridden by an environment variable.
    """

    logger = None

    def __init__(self, name="custom", config_path="logging.json"):
        """
        Initializes the logger instance.

        :param name: The name for the logger instance, defaults to "custom".
        :type name: str, optional
        :param config_path: The path to the logging configuration file,
            defaults to "../logging.json".
        :type config_path: str, optional
        """

        env_log_level = os.environ.get("LOG_LEVEL", None)
        env_config_path = os.environ.get("LOG_CONFIG_PATH", config_path)

        try:
            json_config = os.path.join(os.getcwd(), env_config_path)

            with open(json_config, "r", encoding="utf-8") as file:
                json_string = json.loads(file.read())

            logging.config.dictConfig(json_string)

            self.logger = logging.getLogger(name)

            if env_log_level:
                self.logger.setLevel(getattr(logging, env_log_level))

        except FileNotFoundError:
            self.logger = logging.getLogger()
            self.logger.setLevel(logging.DEBUG)
            self.logger.error(msg=f"Logging configuration file not found: {config_path}")
        except Exception as e:  # pylint: disable=broad-except
            logging.basicConfig(
                level=logging.DEBUG,
                format="%(asctime)s - %(levelname)s - %(message)s",
                handlers=[logging.StreamHandler(stream=sys.stdout)],
            )
            self.logger = logging.getLogger(name)
            self.logger.exception("Failed to configure logging: %s", e)

    def info(self, message, *args):
        """
        Log an INFO message.
        """
        self.logger.info(message, *args)

    def error(self, message, *args):
        """
        Log an ERROR message.
        """
        self.logger.error(message, *args)

    def debug(self, message, *args):
        """
        Log a DEBUG message.
        """
        self.logger.debug(message, *args)

    def warning(self, message, *args):
        """
        Log an WARNING message.
        """
        self.logger.warning(message, *args)

    def critical(self, message, *args):
        """
        Log a CRITICAL message.
        """
        self.logger.critical(message, *args)

    def exception(self, message, *args):
        """
        Log an EXCEPTION message.
        """
        self.logger.exception(message, *args)

    def isEnabledFor(self, level):
        return self.logger.level <= level
