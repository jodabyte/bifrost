import logging
import os
from pprint import pformat
from typing import Any

import yaml

CONFIGS_DIRECTORY_PATH = "pycommons/config/"
RESOURCES_DIRECTORY_PATH = "resources/"
LOGS_DIRECTORY_PATH = "logs/"

if not os.path.exists(LOGS_DIRECTORY_PATH):
    os.makedirs(LOGS_DIRECTORY_PATH)


class Handlers(yaml.YAMLObject):
    yaml_tag = "!Handlers"

    def __init__(self) -> None:
        self.console: bool
        self.file: str

    def __repr__(self):
        return f"{self.__class__.__name__}"
        f"(console={self.console}, file={self.file})"


class Logging(yaml.YAMLObject):
    yaml_tag = "!Logging"

    def __init__(self) -> None:
        self.debug: bool
        self.handlers: Handlers
        self.format: str

    def __repr__(self):
        return f"{self.__class__.__name__}"
        f"(debug={self.debug}, handlers={self.handlers}, format={self.format})"


def load_config(file_name: str) -> Any:
    return yaml.full_load(open(CONFIGS_DIRECTORY_PATH + file_name, "r"))


# global logging configuration
logging_config: Logging = load_config("common.yaml")

root_logger = logging.getLogger()

if logging_config.debug:
    root_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt=logging_config.format)

file_handler = logging.FileHandler(
    f"{LOGS_DIRECTORY_PATH}{logging_config.handlers.file}", mode="w"
)
file_handler.setFormatter(formatter)
root_logger.addHandler(file_handler)
if logging_config.handlers.console:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)

logger = logging.getLogger(__name__)
logger.debug(f"Loaded global config: {pformat(logging_config)}")
