import logging
from collections import deque
from threading import Event
from typing import Callable, Deque, Dict

import webrtcvad
from pycommons.config.config import Config

logger: logging.Logger = logging.getLogger(__name__)


class InterruptEvent(Exception):
    pass


class InsufficientSpeech(Exception):
    pass


class SpeechThresholdExceeded(Exception):
    pass


class SpeechActivityDetection:
    def __init__(self, config: Config, interrupt_event: Event) -> None:
        self.interrupt_event = interrupt_event
        self.vad = webrtcvad.Vad(config.sad.vad_mode)
        self.silence_threshold = config.sad.silence_threshold
        self.min_speech_duration_threshold = config.sad.min_speech_duration_threshold
        self.max_speech_duration_threshold = config.sad.max_speech_duration_threshold
        self.input_device_index = config.sad.input_device_index
        self.frames_per_buffer = config.sad.frames_per_buffer
        self.vad_sampling_rate = config.sad.vad_sampling_rate

    def __call__(self, context: Dict, source: Callable) -> None:
        logger.debug(f"sad with source={source}")
        with source(self.input_device_index, self.frames_per_buffer) as stream:
            recorded_speech: Deque[bytes] = deque()

            try:
                silence_counter = 0
                speech_counter = 0

                for frames in stream.read():
                    if self.interrupt_event.is_set():
                        raise InterruptEvent()

                    recorded_speech.append(frames)
                    is_speech = self.vad.is_speech(frames, self.vad_sampling_rate)
                    logger.debug(f"frame has {'speech' if is_speech else 'no speech'}")

                    if is_speech:
                        silence_counter = 0
                        speech_counter += 1
                        logger.debug(
                            f"silence frame counter reseted\nspeech frame counter increased: {speech_counter}"
                        )
                    else:
                        silence_counter += 1
                        logger.debug(
                            f"silence frame counter increased: {silence_counter}"
                        )

                    if silence_counter > self.silence_threshold:
                        if speech_counter > self.min_speech_duration_threshold:
                            duration = len(recorded_speech) - (
                                self.silence_threshold * 0.9
                            )
                            while len(recorded_speech) > duration:
                                recorded_speech.pop()
                            logger.debug("silence threshold exceeded")
                            break
                        else:
                            raise InsufficientSpeech()
                    elif speech_counter > self.max_speech_duration_threshold:
                        raise SpeechThresholdExceeded()

                context["frames"] = recorded_speech

            except (
                InterruptEvent,
                InsufficientSpeech,
                SpeechThresholdExceeded,
            ) as err:
                logger.error(type(err).__name__)
