#!/usr/bin/env python3
"""
    turret-controller:
    * listen to joystick input
    * grab webcam frames
    * serial output to arduino
"""
from __future__ import print_function
import logging
import state
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
    s = state.State()
    g.deadband_x = j.deadband_x
    g.deadband_y = j.deadband_y
    last_frame_gray = None
    while True:
        ret, frame = c.read()
        if s.tracking:
            # TODO: automated camera object tracking stuff
            # frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # frame = c.detect_blobs(frame)
            # frame = c.track_colour(frame, hue=170)
            # frame, last_frame_gray = c.motion_detect(
            #     frame, frame_gray, last_frame_gray
            # )
            pass
        else:
            s.target_x = j.x
            s.target_y = j.y
        s.fire = j.fire
        s.scanning = False
        s.mode = 1

        a.command_async(
            s.target_x, s.target_y, s.fire, s.mode, s.scanning
        )

        g.target_x = s.target_x
        g.target_y = s.target_y
        g.target_fire = s.fire
        g.target_automatic = s.tracking
        g.status_text_top_left = a.last_string.decode('utf8')
        g.warning_top_left = a.is_hanging()
        if ret:
            g.render(frame)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()