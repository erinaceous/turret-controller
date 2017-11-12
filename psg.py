"""
    psg.py: Code for talking to an Arduino running
    Project Sentry Gun firmware over USB serial
"""
import threading
import logging
import serial
import struct
import time


logger = logging.getLogger(__name__)


class Arduino(threading.Thread):

    def __init__(
            self, serial_path='/dev/ttyACM0', serial_baud=4800,
            setup=True, wait=True, max_retries=3,
            min_x=0, max_x=180,
            min_y=0, max_y=180,
            update_interval=0.1,
            hanging_timeout=3.0
    ):
        super(Arduino, self).__init__()
        self.serial_path = serial_path
        self.serial_baud = serial_baud
        self.wait = wait
        self.serial = None
        if setup:
            self._setup_serial()
        self.last_x = 0
        self.last_y = 0
        self.fire = False
        self.fire_selector = 1
        self.scan_selector = 1
        self.retries = 0
        self.max_retries = max_retries
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.update_interval = update_interval
        self.daemon = True
        self.last_string = ''
        self.hanging_timeout = hanging_timeout
        self.last_command_time = time.time()

    def _setup_serial(self):
        self.serial = serial.Serial(self.serial_path, self.serial_baud)
        if self.wait:
            self._wait_for_T()

    def _wait_for_T(self):
        while True:
            c = self.serial.read()
            if c == b'T':
                return

    def scale(
            self, val, input_min, input_max, output_min, output_max
    ):
        val = float(val)
        return int((
            (output_max - output_min)
            * (val - input_min)
            / (input_max - input_min)
        ) + output_min)

    def run(self):
        while True:
            self.command(
                self.last_x, self.last_y,
                self.fire, self.fire_selector,
                self.scan_selector
            )
            time.sleep(self.update_interval)

    def command_async(
            self, x, y, fire, fire_selector, scan_selector
    ):
        self.last_x = x
        self.last_y = y
        self.fire = fire
        self.fire_selector = fire_selector
        self.scan_selector = scan_selector

    def command(
            self, x, y, fire, fire_selector, scan_selector
    ):
        self.last_x = x
        self.last_y = y
        self.fire = fire
        self.fire_selector = fire_selector
        self.scan_selector = scan_selector
        string = b'a%03d%03d%01d%01d%01d' % (
            self.scale(x, 0, 1.0, self.min_x, self.max_x),
            self.scale(y, 0, 1.0, self.min_y, self.max_y),
            int(fire),
            int(fire_selector),
            int(scan_selector)
        )
        self.last_string = string
        logger.debug('%s -> %s', self.serial_path, string)
        while not self.serial and self.retries < self.max_retries:
            self._setup_serial()
            self.retries += 1
            time.sleep(1)
        if self.serial:
            self._wait_for_T()
            self.serial.write(string)
        else:
            raise BaseException('Serial Device isn\'t talking to us :(')
        self.last_command_time = time.time()

    def is_hanging(self):
        now = time.time()
        return (now - self.hanging_timeout) > self.last_command_time