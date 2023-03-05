####################################################################################################################
# IMPORTS
import pygame
from pygame.key import ScancodeWrapper
from TelloPlus import TelloPlus


# IN CV2 Colors are not defined in RGB but in BGR

class KeyboardController:
    ####################################################################################################################
    # GLOBALS

    # ---> Constants
    TELLO_SPEED = 0.05

    # --> Movements Command
    KEY_MOVE_RIGHT_YAW = "RIGHT"
    KEY_MOVE_LEFT_YAW = "LEFT"
    KEY_MOVE_TAKEOFF = "UP"
    KEY_MOVE_LANDING = "DOWN"

    KEY_MOVE_FORWARD = "w"
    KEY_MOVE_BACKWARD = "s"
    KEY_MOVE_RIGHT_CLOCK = "d"
    KEY_MOVE_LEFT_CLOCK = "a"

    # --> Tello Functions Command
    KEY_TAKEOFF = "t"
    KEY_LANDING = "l"

    KEY_STREAM = "i"
    KEY_SAVE_IMG = "p"

    # ---> Attributes

    ####################################################################################################################
    # CORE

    # ---> Constructor
    def __init__(self, tello_plus: TelloPlus):
        self.tello_plus = tello_plus
        self.key_pressed = None
        # pygame.init()

    # ---> Functions
    def update_pressed(self, key_pressed: ScancodeWrapper):
        self.key_pressed = None
        self.key_pressed = key_pressed

    def if_key_pressed(self, key_name) -> bool:
        # Check if input keyboard has been pressed
        pressed = False

        my_key = getattr(pygame, 'K_{}'.format(key_name))
        if self.key_pressed[my_key]:
            pressed = True

        # pygame.display.update()

        return pressed

    def get_movements(self) -> list[int]:
        """
            Returns an array which contains the movements based on keyboard input
                right_left = Right and Left YAW movement
                forward_backward = Forward and Backward movement
                up_down = Right and Left Clockwise Movement
                yaw_vel = Take-Off and Landing Movement

            Variable name is determined by documentation of
            send_rc_control function of Tello library
        """

        right_left, forward_backward, up_down, yaw_vel = 0, 0, 0, 0
        speed = 100

        # Right and Left YAW movement
        if self.if_key_pressed(self.KEY_MOVE_RIGHT_YAW):
            right_left = speed
        elif self.if_key_pressed(self.KEY_MOVE_LEFT_YAW):
            right_left = -speed

        # Forward and Backward movement
        if self.if_key_pressed(self.KEY_MOVE_FORWARD):
            forward_backward = speed
        elif self.if_key_pressed(self.KEY_MOVE_BACKWARD):
            forward_backward = -speed

        # Right and Left Clockwise Movement
        if self.if_key_pressed(self.KEY_MOVE_RIGHT_CLOCK):
            up_down = speed
        elif self.if_key_pressed(self.KEY_MOVE_LEFT_CLOCK):
            up_down = -speed

        # Take-Off and Landing Movement
        if self.if_key_pressed(self.KEY_MOVE_TAKEOFF):
            yaw_vel = speed
        elif self.if_key_pressed(self.KEY_MOVE_LANDING):
            yaw_vel = -speed

        movements = [right_left, forward_backward, up_down, yaw_vel]
        return movements

    def exe_command(self) -> bool:
        """
            Executes command from keyboard
            -> Take-Off
            -> Landing
            -> Start/Stop Streaming
            -> Capture images saving on desktop
        """
        running = True

        # --> Take-Off
        if self.if_key_pressed(self.KEY_TAKEOFF):
            self.tello_plus.start_streaming()
            self.tello_plus.takeoff()

        # --> Landing
        if self.if_key_pressed(self.KEY_LANDING):
            self.tello_plus.land()
            self.tello_plus.stop_streaming()
            running = False

        # --> Start/Stop Streaming
        if self.if_key_pressed(self.KEY_STREAM):
            if not self.tello_plus.stream_on:
                self.tello_plus.start_streaming()
            else:
                self.tello_plus.stop_streaming()

        # --> Capture Image and Save on Desktop
        if self.tello_plus.stream_on:
            img = self.tello_plus.get_img(0, 0)
            if self.if_key_pressed(self.KEY_SAVE_IMG):
                self.tello_plus.save_img(img)

        # --> Move Tello with keyboard
        if self.tello_plus.is_flying:
            movement = self.get_movements()
            self.tello_plus.send_rc_control(movement[0],
                                            movement[1],
                                            movement[2],
                                            movement[3],
                                            self.TELLO_SPEED)

        return running

    """
    
    """
    
