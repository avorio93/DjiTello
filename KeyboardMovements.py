import cv2
from MyTello import MyTello
import pygame  # pip install pygame==2.0.0.dev6


def init():
    pygame.init()
    win = pygame.display.set_mode((400, 400))


def get_key_pressed(key_name) -> bool:
    # Check if input keyboard has been pressed
    pressed = False

    for events in pygame.event.get(): pass
    key_input = pygame.key.get_pressed()

    my_key = getattr(pygame, 'K_{}'.format(key_name))
    if key_input[my_key]:
        pressed = True

    pygame.display.update()

    return pressed


def get_keyboard_input():

    # Variable name is determined by documentation of
    # send_rc_control function of Tello library
    left_right, forw_backw, up_down, yaw_vel = 0, 0, 0, 0
    speed = 100

    # Right and Left YAW movement
    if get_key_pressed("RIGHT"):
        left_right = speed
    elif get_key_pressed("LEFT"):
        left_right = -speed

    # Forward and Backward movement
    if get_key_pressed("w"):
        forw_backw = speed
    elif get_key_pressed("s"):
        forw_backw = -speed

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

    return [left_right, forw_backw, up_down, yaw_vel]


if __name__ == '__main__':
    init()
    tello = MyTello()

    while True:

        if get_key_pressed("t"):
            tello.takeoff()

        if get_key_pressed("l"):
            if tello.stream_on:
                tello.stop_streaming()
            tello.land()
            break

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
                img = cv2.resize(img, (360, 240))
                cv2.imshow("Tello Image", img)
