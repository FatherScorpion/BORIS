from pose_engine import PoseEngine
from PIL import Image
from PIL import ImageDraw
import cv2

import numpy as np
import os

import time
import threading
from logging import NullHandler

class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

# detect: だれか検知するとTrue
# color: Yellow Red Otherのどれか
# position: position.x = x座標、position.y = y座標
# positionはだいたい胸のあたりの座標
class PoseResult:
    def __init__(self, detect: bool, color: str, position: Position):
        self.detect = detect
        self.color = color
        self.position = position

streamstop = False
tm = NullHandler

engine = PoseEngine('models/mobilenet/posenet_mobilenet_v1_075_481_641_quant_decoder_edgetpu.tflite')
cap = None
ret = None
frame = None

def rgb_to_hue(r, g, b):
    # Convert RGB to normalized values between 0 and 1
    r, g, b = r / 255.0, g / 255.0, b / 255.0

    # Find maximum and minimum values of RGB
    cmax, cmin = max(r, g, b), min(r, g, b)

    # Calculate the range of RGB values
    delta = cmax - cmin

    # Calculate hue based on RGB values
    if delta == 0:
        hue = 0
    elif cmax == r:
        hue = ((g - b) / delta) % 6
    elif cmax == g:
        hue = (b - r) / delta + 2
    else:
        hue = (r - g) / delta + 4

    # Convert hue to degrees and return the value
    hue *= 60
    return int(round(hue))

def get_color_name(hue):
    # Check if hue is in the red range (0-30 or 330-360 degrees)
    if hue >= 0 and hue < 30 or hue >= 355 and hue <= 360:
        return 'Red'
    # Check if hue is in the yellow range (30-60 degrees)
    elif hue >= 30 and hue < 90:
        return 'Yellow'
    # Otherwise, the hue is in a different color range
    else:
        return 'Other'

def camSet():
    global cap,ret,frame
    ret, frame = cap.read()

def job():
    global cap
    cap = cv2.VideoCapture(-1)

    while streamstop == False:
        camSet()
        time.sleep(0.01)

    cap.release()

def savePicture(image):
    image.save("camera.png")

def cv2pil(imgCV):
    imgCV_RGB = imgCV[:, :, ::-1]
    imgPIL = Image.fromarray(imgCV_RGB)
    return imgPIL 

def getPoseFromCamera() -> PoseResult:
    pil_image = cv2pil(frame).convert('RGB')
    # draw = ImageDraw.Draw(pil_image)
    r = 5

    poses, inference_time = engine.DetectPosesInImage(pil_image)
    print('Inference time: %.f ms' % (inference_time * 1000))

    for pose in poses:
        if pose.score < 0.4: continue
        print('\nPose Score: ', pose.score)
        for label, keypoint in pose.keypoints.items():
            print('  %-20s x=%-4d y=%-4d score=%.1f' %(label.name, keypoint.point[0], keypoint.point[1], keypoint.score))
            x,y = keypoint.point[0], keypoint.point[1]
            # draw.ellipse((x-r, y-r, x+r, y+r), fill=(int(255 * keypoint.score), 0, 0))

        items = list(pose.keypoints.values())

        left_shoulder = Position(items[5].point[0],items[5].point[1])
        right_shoulder = Position(items[6].point[0],items[6].point[1])
        left_wrist = Position(items[9].point[0],items[9].point[1])
        right_wrist = Position(items[10].point[0],items[10].point[1])

        if left_wrist.y > left_shoulder.y and right_wrist.y > right_shoulder.y:
            padding = 30
            hidariue = Position(max(min(left_wrist.x, left_shoulder.x, right_wrist.x, right_shoulder.x)-padding, 0),max(min(left_wrist.y, left_shoulder.y, right_wrist.y, right_shoulder.y)-padding,0))
            migisita = Position(min(max(left_wrist.x, left_shoulder.x, right_wrist.x, right_shoulder.x)+padding, 640),min(max(left_wrist.y, left_shoulder.y, right_wrist.y, right_shoulder.y)+padding,480))

            # draw.rectangle((hidariue.x,hidariue.y,migisita.x,migisita.y), outline=(0,255,0))

            red_cnt = 0
            yellow_cnt = 0

            print(int(hidariue.x), int(migisita.x))
            print(int(hidariue.y), int(migisita.y))

            for x in range(int(hidariue.x), int(migisita.x)):
                for y in range(int(hidariue.y), int(migisita.y)):
                    r,g,b = pil_image.getpixel((x,y))
                    hue = rgb_to_hue(r,g,b)
                    p_color = get_color_name(hue)

                    if p_color == 'Red':
                        red_cnt += 1
                    elif p_color == 'Yellow':
                        yellow_cnt += 1
            
            color = 'Other'
            if max(red_cnt,yellow_cnt) > 100:
                if red_cnt > yellow_cnt:
                    color = 'Red'
                else:
                    color = 'Yellow'
            
            target_point = Position((hidariue.x + migisita.x) // 2, (hidariue.y + migisita.y) // 2)
            print(color,red_cnt,yellow_cnt)
            print(target_point.x, target_point.y)
            # pthread = threading.Thread(target=savePicture, kwargs={'image':pil_image})
            # pthread.start()
            return PoseResult(True, color, target_point)

    # pthread = threading.Thread(target=savePicture, kwargs={'image':pil_image})
    # pthread.start()

    return PoseResult(False, "Other", Position(0,0))

def initialize():
    global tm,streamstop,cap
    streamstop = False
    print("start")
    tm = threading.Thread(target=job)
    tm.start()

def disable():
    global streamstop
    streamstop = True

def main():
    initialize()

    while(1):
        hoge = input("next:")
        if hoge == "exit": break

        time.sleep(5)
        getPoseFromCamera()
    
    disable()
    return

if __name__ == "__main__":
    main()
