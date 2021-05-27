import logging
from threading import Event

from pycommons.config.config import RESOURCES_DIRECTORY_PATH, Config
from snowboy import snowboydecoder

logger: logging.Logger = logging.getLogger(__name__)


class Snowboy:
    def __init__(self, config: Config, interrupt_event: Event) -> None:
        self.interrupt_event = interrupt_event
        self.detected = False
        self.hwd = snowboydecoder.HotwordDetector(
            decoder_model=RESOURCES_DIRECTORY_PATH + config.kws.decoder_model,
            sensitivity=config.kws.sensitivity,
            audio_gain=config.kws.audio_gain,
            apply_frontend=config.kws.apply_frontend,
        )

    def __call__(self) -> None:
        logger.info("kws using snowboy")
        self.detected = False
        self.hwd.start(
            interrupt_check=self._interrupt_callback,
            detected_callback=self._detected_callback,
        )
        self.hwd.terminate()

    def _interrupt_callback(self):
        return self.interrupt_event.is_set() or self.detected

    def _detected_callback(self):
        logger.info("hotword detected")
        self.detected = True
