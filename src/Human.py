import time


class Human:
    THRESHOLD_SECS = 3

    def __init__(self, config_human):
        self.face = None
        self.isVisible = False
        self.seenRecently = True
        self.lastSeen = 0
        self.firstSeen = 0
        self.isDisappear = False
        self.THRESHOLD_SECS = config_human['threshold seconds']

    def found(self, face):
        self.face = face
        now = time.time()
        if not self.isVisible:
            self.firstSeen = now
        self.lastSeen = now
        self.isVisible = True
        self.seenRecently = True
        self.isDisappear = False

    def lost(self):
        now = time.time()
        if self.isVisible:
            self.firstSeen = 0
            self.isDisappear = True
        else:
            self.isDisappear = False
        if now - self.lastSeen >= Human.THRESHOLD_SECS:
            self.seenRecently = False
        else:
            self.seenRecently = True
        self.isVisible = False
        pass

    def getFaceCenter(self):
        (x, y, w, h) = self.face
        return x + w / 2, y + h / 2
