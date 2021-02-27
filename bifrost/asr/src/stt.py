import logging
from datetime import datetime
from typing import Dict

import deepspeech as ds
import numpy as np
from pycommons.config import RESOURCES_DIRECTORY_PATH

from config import Config

logger: logging.Logger = logging.getLogger(__name__)


class DeepSpeech:
    class DeepSpeechLogger:
        def __init__(self, config: Config) -> None:
            if config.stt.logger.enable:
                formatter = logging.Formatter(fmt=config.stt.logger.format)
                file_handler = logging.FileHandler(
                    config.stt.logger.file, mode="w"
                )
                file_handler.setFormatter(formatter)

                self.logger: logging.Logger = logging.getLogger(
                    "DeepSpeechLogger"
                )
                self.logger.propagate = False
                self.logger.setLevel(logging.DEBUG)
                self.logger.addHandler(file_handler)

        def log(self, message: str) -> None:
            if self.logger is not None:
                self.logger.debug(message)

    def __init__(self, config: Config) -> None:
        self._model: ds.Model = ds.Model(
            RESOURCES_DIRECTORY_PATH + config.stt.model
        )
        self._model.enableExternalScorer(
            RESOURCES_DIRECTORY_PATH + config.stt.scorer
        )

        self.logger = self.DeepSpeechLogger(config)

    @property
    def sampling_rate(self) -> int:
        return self._model.sampleRate()

    def __call__(self, context: Dict):
        if "frames" in context:
            logger.info("preforming stt")
            ts_start = datetime.now()
            result = self._model.stt(
                np.frombuffer(
                    np.concatenate(context["frames"], axis=None),
                    dtype=np.int16,
                )
            )
            self.logger.log(f"{datetime.now() - ts_start} {result}")
            context["command"] = result
