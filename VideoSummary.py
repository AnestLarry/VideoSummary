import cv2
import sys
from PIL import Image
import numpy as np
from typing import *
import os
from mt import timelib


class VideoSummaryPhoto(object):
    def __init__(self, size: Tuple, framesNum: int):
        self.__nth: int = 0
        self.__gap: int = 10
        self.__frameSize = size
        self.__size: Tuple[int, 2] = (
            size[0] * 5 + 4 * self.__gap,
            size[1] * (framesNum // 5) if size[1] % 5 == 0 else size[1] * (framesNum // 5) + 1
        )
        self.img = Image.new("RGB", self.__size)

    def append(self, img):
        x = 0 if self.__nth % 5 == 0 else (self.__frameSize[0] + self.__gap) * (self.__nth % 5)
        y = (self.__nth // 5) * self.__frameSize[1]
        self.__nth += 1
        self.img.paste(img, (x, y))

    def getImage(self):
        return self.img


if __name__ == '__main__':
    path: str = ""
    spiltSeconds: int = 30
    selectRange: List[int] = [0, 0]
    frames: List = []
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = input("key in your video's file:")
    spiltSeconds = int(input("skip seconds: "))
    if (temp := input("select range(if need)e.g:3,3: ")) != "":
        selectRange = [int(x) for x in temp.split(",")]
    cap = cv2.VideoCapture(path)
    rate = int(cap.get(cv2.CAP_PROP_FPS))


    @timelib.Simple_timelog
    def collecting():
        nth = 1
        cap.set(cv2.CAP_PROP_POS_FRAMES, nth * spiltSeconds * rate)
        stat, frame = cap.read()
        while stat:
            cap.set(cv2.CAP_PROP_POS_FRAMES, nth * spiltSeconds * rate)
            nth += 1
            frames.append(np.asarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            stat, frame = cap.read()


    frameSize = tuple(int(x * 0.15) for x in Image.fromarray(frames[0]).size)
    frames = frames[selectRange[0]:len(frames) - selectRange[1]]
    vsp: VideoSummaryPhoto = VideoSummaryPhoto(frameSize, len(frames))


    @timelib.Simple_timelog
    def Merging():
        for n in range(len(frames)):
            vsp.append(Image.fromarray(frames[n]).resize(frameSize))


    vsp.getImage().save("%s video shot per %d seconds.png" % (os.path.split(path)[1], spiltSeconds))
    os.system("pause")
