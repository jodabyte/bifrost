import logging
import signal
import threading
from enum import Enum, auto

from pycommons.asr import States
from pycommons.audio.seeed4micvoicecard import Seeed4micVoiceCard
from pycommons.audio.source import Microphone
from pycommons.config.config import Config, load_config

from asr.asr.kws import Snowboy
from asr.asr.sad import SpeechActivityDetection
from asr.asr.stt import DeepSpeech


class Handlers(Enum):

    KWS = auto()
    SAD = auto()
    STT = auto()
    SOURCE = auto()


class Service:
    def __init__(self, config: Config) -> None:
        # signals to close app
        self.termination_event = threading.Event()
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        self.handlers = {
            Handlers.KWS: Snowboy(config, self.termination_event),
            Handlers.SAD: SpeechActivityDetection(config, self.termination_event),
            Handlers.STT: DeepSpeech(config),
            Handlers.SOURCE: Microphone(config),
        }
        self.subscribers = {Seeed4micVoiceCard(self.termination_event)}

    def run(self):
        state = States.STANDBY
        session = {}
        state_change_event = threading.Event()

        while not self.termination_event.is_set():
            state_change_event.set()
            for subscriber in self.subscribers:
                state_change_event = threading.Event()
                subscriber(state, state_change_event)

            if state is States.STANDBY:
                session = {}
                self.handlers[Handlers.KWS]()
                state = States.RECORD
            elif state is States.RECORD:
                self.handlers[Handlers.SAD](session, self.handlers[Handlers.SOURCE])
                state = States.TRANSCRIPT
            elif state is States.TRANSCRIPT:
                self.handlers[Handlers.STT](session)
                if "command" in session:
                    logger.info("command = {}".format(session["command"]))
                state = States.STANDBY

        logger.info("termination event recognised")

    def _signal_handler(self, signal_number, frame):
        # logger.info(f"Signal: {signal.strsignal(signal_number)} and {frame}")
        logger.info(f"signal: {signal_number} and {frame}")
        self.termination_event.set()


logger = logging.getLogger(__name__)

if __name__ == "__main__":
    config: Config = load_config("asr.yaml")["asr"]
    logger.debug(f"asr config: {config}")
    service = Service(config)
    service.run()
    logger.info("asr service stoped")
