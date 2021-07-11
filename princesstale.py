import cv2
import numpy as np
from ppadb.client import Client
import mss
import threading
from PIL import Image
import time


def connect_device():
    print("start to connect to device")
    adb = Client(host='127.0.0.1', port=5037)
    print(adb.version())
    print('connect to nox')
    devices = adb.devices()
    print("checking if connect successful")
    if len(devices) == 0:
        print("No connected devices")
        quit()
    print("here")
    print(devices[0])
    return devices[0]

def retry_find(d, delay):
    received_but = (600, 1082)
    tap_anywhere = (600, 1000)
    tap_to_see = (460, 1240)

    click(d, received_but[0], received_but[1], delay)
    click(d, tap_anywhere[0], tap_anywhere[1], delay)
    click(d, tap_to_see[0], tap_to_see[1], delay)

def click(d, x, y, delay):
    time.sleep(delay)
    print("click on {0}-{1}".format(str(x), str(y)))
    d.shell(f'input tap {x} {y}')

device = connect_device()
# ss = device.screencap()
# with open("screen.png", "wb") as fp:
#     fp.write(ss)


# sct = mss.mss()
a = 10
b = 10
c = 100

red_threshold = 2239

while True:
    time.sleep(3)
    image = device.screencap()
    img = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    image = cv2.resize(img, (450, 800))
    # image_check = cv2.rectangle(image, (330, 360), (380, 410), (255, 0, 0), 2)
    image = image[350:420, 320:390]

    # hsvFrame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # img  = np.array(scr)
    
    # if cv2.waitKey(25) == ord('a'):
    #     a = a+10
    # if cv2.waitKey(25) == ord('b'):
    #     b = b+10
    # if cv2.waitKey(25) == ord('c'):
    #     c = c+10

    red_lower = np.array([a, b, c], np.uint8)
    
    red_upper = np.array([200, 200, 255], np.uint8)
    red_mask = cv2.inRange(image, red_lower, red_upper)
    output = cv2.bitwise_and(image, image, mask=red_mask)


    

    cv2.imshow('output', np.hstack([image, output]))

    if cv2.waitKey(25) == ord('q'):
        cv2.destroyAllWindows()
        break
    
    count_red = cv2.countNonZero(red_mask)
    print(count_red)
    if count_red >= red_threshold and count_red != 2377 and count_red != 2365 and count_red != 2317:
        print("FOUND")
        found = True
        break
    else:
        print("RETRY")
        retry_find(device, 1)