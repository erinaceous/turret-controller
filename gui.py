"""
    gui.py: Use OpenCV highgui functions to render a GUI over the
    webcam image.
"""
import cv2


class GUI(object):
    def __init__(
            self, target_x=0.5, target_y=0.5,
            win_width=0, win_height=0,
            win_name='turret'
    ):
        self.target_x = 0.5
        self.target_y = 0.5
        self.target_fire = False
        self.win_width = 0
        self.win_height = 0
        self.win_name = win_name

    def render(self, frame):
        h, w, d = frame.shape
        gui_frame = frame.copy()
        tx = int(self.target_x * w)
        ty = int(self.target_y * h)
        tc = (255, 0, 0)
        if self.target_fire:
            tc = (0, 0, 255)
        gui_frame = cv2.circle(gui_frame, (tx, ty), 32, tc, 2)
        cv2.imshow(self.win_name, gui_frame)