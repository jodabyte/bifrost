import logging
import os
from pprint import pformat
from typing import Any, List, Union

import yaml

CONFIGS_DIRECTORY_PATH = "pycommons/config/"
RESOURCES_DIRECTORY_PATH = "pycommons/resources/"
LOGS_DIRECTORY_PATH = "logs/"

if not os.path.exists(LOGS_DIRECTORY_PATH):
    os.makedirs(LOGS_DIRECTORY_PATH)


class MicrophoneConfig(yaml.YAMLObject):
    yaml_tag = "!microphone"

    def __init__(self) -> None:
        self.sampling_rate: int
        self.sample_format: str
        self.input_device_index: int
        self.frames_per_buffer: int

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(sampling_rate={self.sampling_rate}, "
            f"sample_format={self.sample_format}, "
            f"input_device_index={self.input_device_index}, "
            f"frames_per_buffer={self.frames_per_buffer}"
        )


class SnowboyConfig(yaml.YAMLObject):
    yaml_tag = "!snowboy"

    def __init__(self) -> None:
        self.decoder_model: str
        self.sensitivity: Union[int, List[int]]
        self.audio_gain: float
        self.apply_frontend: bool

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(decoder_model={self.decoder_model}, "
            f"sensitivity={self.sensitivity}"
            f"audio_gain={self.audio_gain}"
            f"apply_frontend={self.apply_frontend}"
        )


class SadConfig(yaml.YAMLObject):
    yaml_tag = "!sad"

    def __init__(self) -> None:
        self.vad_mode: int
        self.vad_sampling_rate: int
        self.silence_threshold: int
        self.min_speech_duration_threshold: int
        self.max_speech_duration_threshold: int
        self.input_device_index: int
        self.frames_per_buffer: int

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(vad_mode={self.vad_mode}, "
            f"vad_sampling_rate={self.vad_sampling_rate}, "
            f"silence_threshold={self.silence_threshold}, "
            "min_speech_duration_threshold="
            f"{self.min_speech_duration_threshold}, "
            "max_speech_duration_threshold="
            f"{self.max_speech_duration_threshold}, "
            "input_device_index="
            f"{self.input_device_index}, "
            "frames_per_buffer="
            f"{self.frames_per_buffer}"
        )


class DeepSpeechLoggerConfig(yaml.YAMLObject):
    yaml_tag = "!deepspeechlogger"

    def __init__(self) -> None:
        self.enable: bool
        self.file: str
        self.format: str

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(enable={self.enable}, "
            f"file={self.file}, format={self.format}"
        )


class DeepSpeechConfig(yaml.YAMLObject):
    yaml_tag = "!deepspeech"

    def __init__(self) -> None:
        self.model: str
        self.scorer: str
        self.logger: DeepSpeechLoggerConfig

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(model={self.model}, "
            f"scorer={self.scorer}, logger={self.logger}"
        )


class Config(yaml.YAMLObject):
    yaml_tag = "!asr"

    def __init__(self) -> None:
        self.source: MicrophoneConfig
        self.kws: SnowboyConfig
        self.sad: SadConfig
        self.stt: DeepSpeechConfig

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(source={self.source}, "
            f"kws={self.kws}, sad={self.sad}, stt={self.stt})"
        )


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
