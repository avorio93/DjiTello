import time

import cv2
import time
import os
from MyTello import MyTello
import pygame  # pip install pygame==2.0.0.dev6

global img


def init():
    pygame.init()
    pygame.display.set_mode((400, 400))


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

    # Right and Left YAW movement
    if get_key_pressed("RIGHT"):
        left_right = speed
    elif get_key_pressed("LEFT"):
        left_right = -speed

    # Forward and Backward movement
    if get_key_pressed("w"):
        forward_backward = speed
    elif get_key_pressed("s"):
        forward_backward = -speed

    # Right and Left Clockwise Movement
    if get_key_pressed("d"):
        up_down = speed
    elif get_key_pressed("a"):
        up_down = -speed

    # Take-Off and Landing Movement
    if get_key_pressed("UP"):
        yaw_vel = speed
    elif get_key_pressed("DOWN"):
        yaw_vel = -speed

    return [left_right, forward_backward, up_down, yaw_vel]


if __name__ == '__main__':
    init()
    tello = MyTello()

    running = True

    while running:

        if get_key_pressed("t"):
            tello.takeoff()
            tello.start_streaming()

        if get_key_pressed("l"):
            if tello.stream_on:
                tello.stop_streaming()
            tello.land()
            running = False

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
