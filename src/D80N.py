import sys

from cv2 import cv2

from src.CamReaderAsync import CamReaderAsync

sys.path.append('../pysca')

from pysca import pysca


class D80N:
    DEFAULT_SPEED = 10
    CENTER_RATIO = 0.15
    HOME_PAN_POS = 0
    HOME_TILT_POS = 0
    HOME_ZOOM = 0

    def __init__(self, config_cam):
        pysca.connect(config_cam['socket'])
        self.videosource = cv2.VideoCapture(config_cam['dev video'])
        self.reader = CamReaderAsync(self.videosource, config_cam['fps smooth ratio'])
        self.atHome = True
        self.DEFAULT_SPEED = config_cam['default speed']
        self.CENTER_RATIO = config_cam['center ratio']
        self.HOME_PAN_POS = config_cam['home pan']
        self.HOME_TILT_POS = config_cam['home tilt']
        self.HOME_ZOOM = config_cam['home zoom']
        pass

    def goHome(self, speed=DEFAULT_SPEED, homeZome=HOME_ZOOM):
        pysca.pan_tilt(1, 0, 0, blocking=True)
        pysca.pan_tilt(1, speed, speed, self.HOME_PAN_POS, self.HOME_TILT_POS, blocking=True)
        pysca.set_zoom(1, homeZome, blocking=True)
        self.atHome = True

    def move(self, speedX=None, speedY=None):
        pysca.pan_tilt(1, speedX, speedY)
        self.atHome = False
        return None

    def stop_tracking_motion(self):
        pysca.pan_tilt(1, 0, 0, blocking=True)

    def Read(self):
        frame = self.videosource.read()
        return frame

    def stop(self):
        self.reader._stop = True
        pass
