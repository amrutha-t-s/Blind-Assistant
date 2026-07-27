import cv2
from config import *

def start_camera():

    cap = cv2.VideoCapture(CAMERA_ID)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not cap.isOpened():
        print("Camera Not Found")
        return None

    print("Camera Started")

    return cap