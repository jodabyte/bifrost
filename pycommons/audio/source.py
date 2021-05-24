import logging
from enum import Enum
from queue import Queue
from types import TracebackType
from typing import Dict, Generator, List, Optional, Type, Union

import pyaudio
from config import Config

logger: logging.Logger = logging.getLogger(__name__)


class SampleFormat(Enum):
    INT16 = pyaudio.paInt16


CONFIG_SAMPLE_FORMATS = {"int16": SampleFormat.INT16}


def get_input_devices() -> List[Dict]:
    source = pyaudio.PyAudio()
    device_count = source.get_device_count()
    device_apis = []
    for index in range(device_count):
        info = source.get_device_info_by_index(index)
        if info["maxInputChannels"] > 0:
            device_apis.append(info)
    source.terminate()
    return device_apis


def get_input_device_by_name(name: str) -> Union[Dict, None]:
    source = pyaudio.PyAudio()
    device_count = source.get_device_count()
    device = None
    for index in range(device_count):
        info = source.get_device_info_by_index(index)
        if info["name"] is name:
            device = info
            break
    source.terminate()
    return device

class Microphone:
    def __init__(self, config: Config) -> None:
        self.sampling_rate = config.source.sampling_rate
        self.sample_format = CONFIG_SAMPLE_FORMATS[config.source.sample_format]
        self.input_device_index = config.source.input_device_index
        self.frames_per_buffer = config.source.frames_per_buffer

    def read(
        self,
    ) -> Generator[bytes, None, None]:
        logger.info("begin reading stream")
        while not self._stream.is_stopped() and self._stream.is_active():
            yield self._queue.get()
        logger.info("finished reading stream")

    def _callback(
        self,
        in_data: bytes,
        frame_count: int,
        time_info: dict,
        status_flags: int,
    ):
        self._queue.put(in_data)
        return (
            None,
            pyaudio.paContinue,
        )

    def __call__(
        self, input_device_index=None, frames_per_buffer=None
    ) -> "Microphone":
        logger.debug(
            f"params: input_device_index={input_device_index}, frames_per_buffer={frames_per_buffer}"
        )

        self._source = pyaudio.PyAudio()
        self._stream = self._source.open(
            rate=self.sampling_rate,
            channels=1,
            format=self.sample_format.value,
            input=True,  # Set Stream as Input Stream
            input_device_index=self.input_device_index
            if input_device_index is None
            else input_device_index,
            frames_per_buffer=self.frames_per_buffer
            if frames_per_buffer is None
            else frames_per_buffer,
            start=False,  # Dont start recording immediately
            stream_callback=self._callback,
        )
        return self

    def __enter__(self):
        logger.info("enter source")
        self._queue = Queue()

        self._stream.start_stream()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ):
        logger.info("exit source")
        self._stream.stop_stream()
        self._stream.close()
        self._source.terminate()
        self._queue = None

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(_sampling_rate={self.sampling_rate}, "
            f"_sample_format={self.sample_format}, "
            f"_input_device_index={self.input_device_index}, "
            "_frames_per_buffer="
            f"{self.frames_per_buffer}"
        )
