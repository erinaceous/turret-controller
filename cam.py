"""
    cam.py: Webcam input
"""
import cv2


class Cam(object):
    def __init__(self, cam_idx=0, mode=cv2.CAP_MODE_GRAY):
        self.cap = cv2.VideoCapture(cam_idx)

    def read(self):
        return self.cap.read()