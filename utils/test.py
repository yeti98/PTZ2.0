# import cv2
#
# from utils.CamReaderAsync import CamReaderAsync
#
#
# cvcamera = cv2.VideoCapture(0)
# reader = CamReaderAsync(cvcamera)
# while True:
#     reader.read()

# class T:
#     a=1
#     def __init__(self):
#         self.b = 1
#         self.c = 2
#     def update(self, **kwargs):
#         if len(kwargs) == 0:
#             return
#         for k, v in kwargs.items():
#             self.__dict__[k]=v
#
# x = T()
# x.update(a=9, c=-1)
# print(x.a)
# print(x.b)
# print(x.c)


# import json
#
# with open('/home/ddragon/PycharmProjects/PTZ2.0/config/config.json', 'r') as handle:
#     x = json.load(handle)
# handle.close()
# print(x)
