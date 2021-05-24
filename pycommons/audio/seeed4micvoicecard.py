import logging
import threading
from queue import Queue
from threading import Event
from typing import Tuple

from apa102_pi.colorschemes import colorschemes
from gpiozero import LED
from pycommons.asr import States

logger = logging.getLogger(__name__)


class Seeed4micVoiceCard:

    NUM_LED = 12

    def __init__(self, interrupt_event: Event) -> None:

        self.interrupt_event = interrupt_event

        # LEDs power switch
        self.power = LED(5)

        self.queue: Queue = Queue()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def __call__(self, state: States, state_change_event: Event) -> None:
        logger.debug(f"state {state}")
        if state in [States.RECORD, States.TRANSCRIPT]:
            self._led_on()
            self.queue.put((state, state_change_event))
        else:
            self._led_off()

    def _run(self):
        logger.debug(f"cycle handler started")
        while not self.interrupt_event.is_set():
            logger.info(f"wait for state")
            item: Tuple[States, Event] = self.queue.get()
            state, state_change_event = item
            logger.info(f"state received:{item}")

            logger.info(f"start led cycle")
            while not state_change_event.is_set():
                if state in [States.RECORD, States.TRANSCRIPT]:
                    cycle = colorschemes.TheaterChase(
                        num_led=self.NUM_LED,
                        pause_value=0.04,
                        num_steps_per_cycle=48,
                        num_cycles=1,
                        order="bgr",
                    )
                    cycle.start()
            logger.info(f"finished led cycle")
        logger.debug(f"cycle handler finished")

    def _led_on(self):
        if not self.power.is_active:
            self.power.on()
            logger.debug(f"led on")

    def _led_off(self):
        if self.power.is_active:
            self.power.off()
            logger.debug(f"led off")
