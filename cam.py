"""
    cam.py: Webcam input
"""
import numpy as np
import cv2


class Cam(object):
    def __init__(self, cam_idx=0, mode=cv2.CAP_MODE_GRAY):
        self.cap = cv2.VideoCapture(cam_idx)
        self.blob_x = 0.5
        self.blob_y = 0.5
        self.detector = cv2.SimpleBlobDetector_create()
        self.keypoints = None

    def read(self):
        return self.cap.read()

    def detect_blobs(self, frame):
        self.keypoints = self.detector.detect(frame)
        im_with_keypoints = cv2.drawKeypoints(
            frame,
            self.keypoints,
            np.array([]),
            (0, 0, 255),
            cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
        )
        return im_with_keypoints