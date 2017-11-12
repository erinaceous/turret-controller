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
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.status_text_top_left = ''
        self.warning_top_left = False

    def render(self, frame):
        h, w, d = frame.shape
        gui_frame = frame.copy()
        tx = int(self.target_x * w)
        ty = int(self.target_y * h)
        tc = (255, 0, 0)
        if self.target_fire:
            tc = (0, 0, 255)
        gui_frame = cv2.circle(gui_frame, (tx, ty), 32, tc, 2)
        top_left_color = (255, 255, 255)
        if self.warning_top_left:
            top_left_color = (0, 0, 255)
        cv2.putText(
            gui_frame,
            self.status_text_top_left,
            (16, 16),
            self.font,
            0.4,
            top_left_color,
            1,
            cv2.LINE_AA
        )
        cv2.imshow(self.win_name, gui_frame)