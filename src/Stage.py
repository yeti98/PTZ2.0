class Stage:
    isCentered = True
    isFarLeft = False
    isFarRight = False
    isFarUp = False
    isFarDown = False
    status = "CENTERED"

    def __init__(self):
        self.status = "CENTERED"
        pass

    def reset(self):
        self.__init__()

    def update(self, **kwargs):
        if len(kwargs) > 0:
            for k, v in kwargs.items():
                self.__dict__[k] = v
            # self.refresh()

    def refresh(self):
        if self.isFarLeft:
            if self.isFarUp:
                # print("Object left up")
                self.status = "LEFT_UP"
            elif self.isFarDown:
                # print("Object left down")
                self.status = "LEFT_DOWN"
            else:
                # print("Object left")
                self.status = "LEFT"

        elif self.isFarRight:
            if self.isFarUp:
                # print("Object right up")
                self.status = "RIGHT_UP"
            elif self.isFarDown:
                # print("Object right down")
                self.status = "RIGHT_DOWN"
                pass
            else:
                # print("Object right")
                self.status = "RIGHT"
        else:
            self.status = "CENTERED"
