import cv2


def detect_usb_camera(max_try=5):
    found = []
    for i in range(0, max_try):
        temp = None
        try:
            temp = cv2.VideoCapture(i)
        except:
            print("Open failed: " + str(i))
        finally:
            if temp:
                if temp.isOpened():
                    temp.release()
                    found.append(i)
    print("Found {} camera(s) at: {}".format(len(found), found))


def testCam(i=0):
    import cv2
    cap = cv2.VideoCapture(i)
    print("Press 'q' to exit...")
    while True:
        ret, frame = cap.read()
        cv2.imshow("frame", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    #     detect_usb_camera()
    testCam()
