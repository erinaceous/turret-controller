#!/usr/bin/env python3
"""
    turret-controller:
    * listen to joystick input
    * grab webcam frames
    * serial output to arduino
"""
from __future__ import print_function
import logging
import time
import cam
import cv2
import gui
import joy
import psg


log_lvl = logging.WARNING


logging.basicConfig(level=log_lvl)
psg.logger.setLevel(log_lvl)


def main():
    print('Hit Ctrl+C in this window to quit the program properly')
    a = psg.Arduino()
    j = joy.Joy()
    j.start()
    a.start()
    c = cam.Cam()
    g = gui.GUI()

    while True:
        a.command_async(
            j.x, j.y, j.fire, 1, 1
        )
        ret, frame = c.read()
        g.target_x = j.x
        g.target_y = j.y
        g.target_fire = j.fire
        # frame = c.detect_blobs(frame)
        g.status_text_top_left = a.last_string.decode('utf8')
        g.warning_top_left = a.is_hanging()
        if ret:
            g.render(frame)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()