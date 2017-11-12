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
        self.last_frame = None

    def read(self):
        ret, frame = self.cap.read()
        if ret:
            self.last_frame = frame
        return ret, frame

    def motion_detect(self, frame, frame_gray, last_frame_gray):
        frame_gray = cv2.blur(frame_gray, (5, 5))
        if last_frame_gray is None:
            return frame, frame_gray

        # params for ShiTomasi corner detection
        feature_params = dict(maxCorners=10,
                              qualityLevel=0.1,
                              minDistance=15,
                              blockSize=15)

        # Parameters for lucas kanade optical flow
        lk_params = dict(winSize=(15, 15),
                         maxLevel=2,
                         criteria=(
                             cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
                         )

        p0 = cv2.goodFeaturesToTrack(
            last_frame_gray, **feature_params
        )
        p1, st, err = cv2.calcOpticalFlowPyrLK(
            last_frame_gray, frame_gray, p0, None, **lk_params
        )
        good_new = p1[st == 1]
        good_old = p0[st == 1]
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            frame = cv2.circle(frame, (a, b), 5, (0, 255, 0), -1)
        return frame, frame_gray

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

    def track_colour(self, frame, hue, tolerance=0.1):
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        tol_lower = int(hue - (180 * tolerance))
        tol_upper = int(hue + (180 * tolerance))
        if tol_lower < 0:
            tol_lower = 0
        if tol_upper > 180:
            tol_upper = 180
        frame_thresh = cv2.inRange(
            frame_hsv[:, :, 0],
            tol_lower,
            tol_upper
        )
        frame_thresh_erode_dilate = cv2.erode(
            frame_thresh,
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        )
        frame_thresh_erode_dilate = cv2.dilate(
            frame_thresh_erode_dilate,
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        )
        frame_thresh_rgb = cv2.cvtColor(
            frame_thresh_erode_dilate, cv2.COLOR_GRAY2BGR
        )
        return frame_thresh_rgb
