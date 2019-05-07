import time

import math

import cv2
import imutils

from src.D80N import D80N
from src.Human import Human
from src.Stage import Stage

HAAR_MODEL = '../model/haarcascade_frontalface_default.xml'


class TrackingModel:
    IMAGE_WIDTH = 0
    IMAGE_HEIGHT = 0
    FRAME_CENTER_X = 0
    FRAME_CENTER_Y = 0
    MARGIN_RATIO = 0.05
    DEBUG_MODE = True
    CENTER_RATIO = 0.15

    def __init__(self, config):
        self.camera = D80N(config['camera'])
        self.human = Human(config['human'])
        self.stage = Stage()
        self.IMAGE_HEIGHT = config['model']['image height']
        self.IMAGE_WIDTH = config['model']['image width']
        self.MARGIN_RATIO = config['model']['margin ratio']
        self.DEBUG_MODE = config['model']['debug mode']
        self.FRAME_CENTER_Y = self.IMAGE_HEIGHT / 2
        self.FRAME_CENTER_X = self.IMAGE_WIDTH / 2
        pass

    def detect(self, gray_img):
        _ = cv2.CascadeClassifier(HAAR_MODEL)
        faces = _.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return faces

    def track(self):
        while True:
            raw_frame = self.camera.Read()
            if raw_frame:
                raw_frame = imutils.resize(raw_frame, width=self.IMAGE_WIDTH)
                gray_img = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2GRAY)
                faces = self.detect(gray_img)
                if len(faces):
                    (x, y, w, h) = faces[0]
                    cv2.rectangle(raw_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    self.human.found((x, y, w, h))
                else:
                    self.human.lost()
                # Evaluate frame
                diff_x, diff_y = self.evaluate()
                # Action Control
                self.decideAction(faces, diff_x, diff_y)
                if TrackingModel.DEBUG_MODE:
                    keyPress = cv2.waitKey(1)
                    if keyPress != -1:
                        keyPress = keyPress & 0xFF
                    if keyPress == ord("q"):
                        self.destroy()
        pass

    def destroy(self):
        try:
            if self.camera:
                self.camera.stop()
                time.sleep(1)
                cv2.destroyAllWindows()
        except Exception as e:
            if TrackingModel.DEBUG_MODE:
                print(e)
            else:
                pass

    def evaluate(self):
        isVisible = self.human.isVisible
        if not isVisible:
            if not self.human.seenRecently:
                self.human.face = None
                self.stage.reset()
        else:
            x_coordinate, y_coordinate = self.human.getFaceCenter()
            diff_x = abs(TrackingModel.FRAME_CENTER_X - x_coordinate)
            diff_y = abs(TrackingModel.FRAME_CENTER_Y - y_coordinate)
            distance = math.sqrt(diff_x ** 2 + diff_y ** 2)
            R = TrackingModel.CENTER_RATIO * TrackingModel.IMAGE_HEIGHT
            if distance <= R:
                self.stage.update(isCentered=True, status='CENTERED')
            else:
                border_left = TrackingModel.FRAME_CENTER_X - TrackingModel.MARGIN_RATIO * TrackingModel.IMAGE_WIDTH
                border_right = TrackingModel.FRAME_CENTER_X + TrackingModel.MARGIN_RATIO * TrackingModel.IMAGE_WIDTH
                border_up = TrackingModel.FRAME_CENTER_Y + TrackingModel.MARGIN_RATIO * TrackingModel.IMAGE_HEIGHT
                border_down = TrackingModel.FRAME_CENTER_Y - TrackingModel.MARGIN_RATIO * TrackingModel.IMAGE_HEIGHT
                if y_coordinate > border_up:
                    self.stage.update(isFarUp=False, isFarDown=True)
                elif y_coordinate < border_down:
                    self.stage.update(isFarUp=True, isFarDown=False)
                else:
                    self.stage.update(isFarUp=False, isFarDown=False)

                if x_coordinate > border_left:
                    self.stage.update(isFarLeft=False, isFarRight=True)
                elif x_coordinate < border_right:
                    self.stage.update(isFarLeft=True, isFarRight=False)
                self.stage.update(isCentered=False)
            self.stage.refresh()

        if TrackingModel.DEBUG_MODE:
            print("****** Evaluate func ******")
            for k, v in self.stage.__dict__.items():
                print("Attr: {} \t is {}".format(k, v))
            print("***************************")
        if isVisible:
            return diff_x, diff_y
        return None, None

    def decideAction(self, faces, diff_x, diff_y):
        if len(faces) >= 3 or not self.human.seenRecently or self.stage.isCentered:
            # print "Stop tracking motion"
            self.camera.stop_tracking_motion()
            return
        if not self.human.seenRecently:
            if not self.camera.atHome:
                # print("Moving to home position")
                self.camera.goHome()
            return
        if diff_x and diff_y:
            speed = self.camera.DEFAULT_SPEED
            speed_x = speed
            speed_y = speed
            if diff_x + diff_y > 0:
                speed_x = speed * (diff_x / (diff_x + diff_y))
                speed_y = speed * (diff_y / (diff_x + diff_y))
            speed_x = round(speed_x, 0)
            speed_y = round(speed_y, 0)
            switcher = {
                'LEFT': self.camera.move(-speed),
                'LEFT_UP:': self.camera.move(-speed_x, +speed_y),
                'LEFT_DOWN': self.camera.move(-speed_x, -speed_y),
                'RIGHT': self.camera.move(speed),
                'RIGHT_UP': self.camera.move(+speed_x, +speed_y),
                'RIGHT_DOWN': self.camera.move(+speed_x, -speed_y),
                'CENTERED': None
            }
            # excute
            switcher.get(self.stage.status)
            return
