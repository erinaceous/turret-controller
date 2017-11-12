"""
    psg.py: Code for talking to an Arduino running
    Project Sentry Gun firmware over USB serial
"""
import logging
import serial
import struct
import time


logger = logging.getLogger(__name__)


class Arduino(object):

    def __init__(
            self, serial_path='/dev/ttyACM0', serial_baud=4800,
            setup=True, wait=True, max_retries=3,
            min_xy=0, max_xy=255
    ):
        self.serial_path = serial_path
        self.serial_baud = serial_baud
        self.wait = wait
        self.serial = None
        if setup:
            self._setup_serial()
        self.last_x = 0
        self.last_y = 0
        self.fire = False
        self.fire_selector = 0
        self.scan_selector = 0
        self.retries = 0
        self.max_retries = max_retries
        self.min_xy = min_xy
        self.max_xy = max_xy

    def _setup_serial(self):
        self.serial = serial.Serial(self.serial_path, self.serial_baud)
        if self.wait:
            self._wait_for_T()

    def _wait_for_T(self):
        while True:
            c = self.serial.read()
            if c == b'T':
                return

    def scale_xy(self, val):
        if val > 1.0:
            val = 1.0
        if val < 0.0:
            val = 0.0

        return int(val * self.max_xy)

    def command(
            self, x, y, fire, fire_selector, scan_selector
    ):
        self.last_x = x
        self.last_y = y
        self.fire = fire
        self.fire_selector = fire_selector
        self.scan_selector = scan_selector
        string = b'a%03d%03d%01d%01d%01d' % (
            self.scale_xy(x),
            self.scale_xy(y),
            int(fire),
            int(fire_selector),
            int(scan_selector)
        )
        logger.info('%s -> %s', self.serial_path, string)
        while not self.serial and self.retries < self.max_retries:
            self._setup_serial()
            self.retries += 1
            time.sleep(1)
        if self.serial:
            self._wait_for_T()
            self.serial.write(string)
        else:
            raise BaseException('Serial Device isn\'t talking to us :(')