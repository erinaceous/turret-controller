#!/usr/bin/env python3
"""
    turret-controller:
    * listen to joystick input
    * grab webcam frames
    * serial output to arduino
"""
import logging
import time
import joy
import psg


log_lvl = logging.DEBUG


logging.basicConfig(level=log_lvl)
psg.logger.setLevel(log_lvl)


def main():
    a = psg.Arduino()
    j = joy.Joy()
    j.start()
    while True:
        a.command(
            j.x, j.y, j.fire, 3, 0
        )
        time.sleep(0.2)


if __name__ == '__main__':
    main()