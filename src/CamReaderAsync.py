import time
from threading import Lock, Thread


class FrameUtils:
    SMOOTH_RATIO = 0.95
    start_time = 0
    frame_rate = 0

    def __init__(self, fps_smooth_ratio):
        self.SMOOTH_RATIO = fps_smooth_ratio
        pass

    def tick(self):
        now = time.time()
        if self.start_time == 0:
            self.start_time = now
        else:
            # TODO: check frame rate calculation method
            frame_rate = 1.0 / (now - self.start_time)
            self.start_time = now
            self.frame_rate = (self.frame_rate + frame_rate) / 2 * FrameUtils.SMOOTH_RATIO
            print(self.get_frame_rate())

    def get_frame_rate(self):
        return self.frame_rate

    pass


class CamReaderAsync:
    def __init__(self, source, smooth_ratio):
        self._locker = Lock()
        self._source = source
        self.fps = FrameUtils(smooth_ratio)
        self.start()

    def start(self):
        self._lastFrameRead = False
        self._frame = None
        self._stop = False
        Thread(self._read()).start()
        pass

    def read(self):
        try:
            self._locker.acquire()
            if not self._lastFrameRead:
                self._lastFrameRead = True
                return self._frame
            return None
        finally:
            self._locker.release()

    def _read(self):
        while True:
            if self._stop:
                return
            ret, frame = self._source.read()
            if ret:
                try:
                    self._locker.acquire()
                    # TODO: add self.fps.tick()s
                    self.fps.tick()
                    self._frame = frame
                    self._lastFrameRead = False
                except Exception as e:
                    print(e)
                finally:
                    self._locker.release()
