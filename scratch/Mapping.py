import math
import time
from typing import Tuple

import cv2
import time
import os
from TelloPlus import TelloPlus
import pygame  # pip install pygame==2.0.0.dev6
import numpy

global img

# IN CV2 Colors are not defined in RGB but in BGR


# PARAMETERS
##########################################################
forwardSpeed = 117 / 10  # Forward speed in cm/s ( 15cm/s )
angSpeed = 369 / 10  # Angular Speed in Degrees/s ( 50d/s )

mappingInterval = 0.25
distanceInterval = forwardSpeed * mappingInterval
angSpeedInterval = angSpeed * mappingInterval

x, y = 0, 0
angle = 0
yaw = 0
points = [(x, y)]
##########################################################

def init():
    pygame.init()
    pygame.display.set_mode((100, 100))


def get_key_pressed(key_name) -> bool:
    # Check if input keyboard has been pressed
    pressed = False

    for _ in pygame.event.get():
        pass
    key_input = pygame.key.get_pressed()

    my_key = getattr(pygame, 'K_{}'.format(key_name))
    if key_input[my_key]:
        pressed = True

    pygame.display.update()

    return pressed


def get_keyboard_input():
    # Variable name is determined by documentation of
    # send_rc_control function of Tello library
    left_right, forward_backward, up_down, yaw_vel = 0, 0, 0, 0
    speed = 100
    distance = 0
    global yaw
    global angle
    global x
    global y

    # Right and Left YAW movement
    if get_key_pressed("RIGHT"):
        left_right = speed
        yaw += angSpeedInterval
    elif get_key_pressed("LEFT"):
        left_right = -speed
        yaw -= angSpeedInterval

    # Forward and Backward movement
    if get_key_pressed("w"):
        forward_backward = speed
        distance = distanceInterval
        angle = 270
    elif get_key_pressed("s"):
        forward_backward = -speed
        distance = -distanceInterval
        angle = -90

    # Right and Left Clockwise Movement
    if get_key_pressed("d"):
        up_down = speed
        distance = -distanceInterval
        angle = 180
    elif get_key_pressed("a"):
        up_down = -speed
        distance = distanceInterval
        angle = -180

    # Take-Off and Landing Movement
    if get_key_pressed("UP"):
        yaw_vel = speed
    elif get_key_pressed("DOWN"):
        yaw_vel = -speed

    # time.sleep(mappingInterval)
    angle += yaw
    x += int(distance*math.cos(math.radians(angle)))
    y += int(distance*math.sin(math.radians(angle)))

    return [left_right, forward_backward, up_down, yaw_vel]


def drawPoints():
    # cv2.circle(img, (x, y), 5, (0, 0, 255), cv2.FILLED)
    for point in points:
        cv2.circle(img, (point[0], point[1]), 5, (255, 0, 0), cv2.FILLED)

    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'({points[-1][0] - 500/100}, {points[-1][1] - 500/100})m',
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1,
                (255, 0, 255) , 1)


if __name__ == '__main__':
    init()
    # tello = TelloPlus()

    running = True

    while running:

        # if get_key_pressed("t"):
        # tello.takeoff()
        # tello.start_streaming()

        if get_key_pressed("l"):
            # if tello.stream_on:
            # tello.stop_streaming()
            # tello.land()
            running = False

        kbInput = get_keyboard_input()
        img = numpy.zeros((480, 720, 3), numpy.uint8)
        point = (x, y)

        if points[-1] != point:
            points.append(point)
        drawPoints()
        cv2.imshow("Output", img)
        cv2.waitKey(1)

'''
        if tello.is_flying:
            kbInput = get_keyboard_input()
            tello.send_rc_control(kbInput[0], kbInput[1], kbInput[2], kbInput[3], 0.05)


            if get_key_pressed("i"):
                if not tello.stream_on:
                    tello.start_streaming()
                else:
                    tello.stop_streaming()

            if tello.stream_on:
                img = tello.get_frame_read().frame
                # img = cv2.resize(img, (360, 240))
                cv2.imshow("Tello Image", img)

                if get_key_pressed("p"):
                    img_name = f'\\{time.time()}.jpg'
                    out_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
                    out_path = out_path + '\\TelloCaptures'
                    if not os.path.isdir(out_path):
                        os.makedirs(out_path)

                    out_path = out_path + img_name

                    cv2.imwrite(out_path, img)
                    time.sleep(0.3)
                    print('frame captured:', out_path)
'''
