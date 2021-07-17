import cv2
import numpy as np
from ppadb.client import Client
import mss
import threading
from PIL import Image
import time

is_pixel = False

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
    if is_pixel:
        received_but = (1000, 1900)
        tap_anywhere = (1000, 1900)
        tap_to_see = (720, 2360)
    else:
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

red_threshold = 2239

while True:
    time.sleep(1)
    image = device.screencap()
    img = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    # pixel 2 xl = 2880 x 1440
    if is_pixel:
        image = img[1300:1490, 1040:1230]
    else:
        _image = cv2.resize(img, (450, 800))
        image = _image[350:420, 320:390]
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    red_lower = np.array([169, 100, 100])
    red_upper = np.array([189, 255, 255])
    red_mask = cv2.inRange(hsv, red_lower, red_upper)
# else:
    #     image = cv2.resize(img, (450, 800))
    #     image = image[350:420, 320:390]
    #     red_lower = np.array([10, 10, 100], np.uint8)
    #     red_upper = np.array([200, 200, 255], np.uint8)
    #     red_mask = cv2.inRange(image, red_lower, red_upper)
    #     output = cv2.bitwise_and(image, image, mask=red_mask)
    
    # if not is_pixel:
        # cv2.imshow('output', np.hstack([image, output]))
    # else:
    cv2.imshow('mask', red_mask)

    if cv2.waitKey(25) == ord('q'):
        cv2.destroyAllWindows()
        break
    
    count_red = cv2.countNonZero(red_mask)
    print(count_red)
    # if count_red >= red_threshold and count_red != 2377 and count_red != 2365 and count_red != 2317 and is_pixel == False:
    #     print("FOUND")
    #     found = True
    #     break
    if count_red >= 70:
        print("Found in pixel2")
        found = True
        break
    else:
        print("RETRY")
        retry_find(device, 1)