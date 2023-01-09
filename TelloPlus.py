####################################################################################################################
# IMPORTS
import os
import time

from djitellopy import tello, BackgroundFrameRead
from time import sleep
from CustomLogger import CustomLogger
from win32api import GetSystemMetrics
import cv2  # If not working, add the path manually to the interpreter


class TelloPlus(tello.Tello):
    """
        This class adds some utils such as a custom logger
        and some parameters to simplify basic movement

        For more detailed documentation, see the original class djitellopy.tello class
    """

    ####################################################################################################################
    # GLOBALS

    # ---> Constants
    CRITICAL_BATTERY = 15
    WARNING_BATTERY = 35
    LOG_NAME = "TELLO_PLUS"

    # ---> Attributes

    ####################################################################################################################
    # CORE

    # ---> Constructor
    def __init__(self):

        # Logger init
        self.logger = CustomLogger(self.LOG_NAME, write_file=False).logger

        # Create a Tello instance and connect it to the drone
        self.logger.info("Initialization...")
        super().__init__()

        try:
            self.logger.info("Connecting to Tello...")
            self.connect()
        except Exception:
            self.logger.critical("Connection refused")
            raise Exception()

        if self.get_battery() > 0:
            self.logger.info("Successfully connected!")
        else:
            self.logger.error("Connection refused")
            raise Exception()

        # Check if drone is ready to Take-Off
        self.logger.info("Battery Level:" + str(self.get_battery()))
        if self.get_battery() >= TelloPlus.CRITICAL_BATTERY:
            if self.get_battery() <= TelloPlus.WARNING_BATTERY:
                self.logger.warning("Low Battery Level")
            self.logger.info("Ready to fly!")

        else:
            self.logger.error("Battery level too low: unable to Take-Off")
            raise Exception()

    # ---> Functions
    # @dispatch(tello.Tello, int, int, int, int, float)
    def send_rc_control(self,
                        left_right_velocity: int,
                        forward_backward_velocity: int,
                        up_down_velocity: int,
                        yaw_velocity: int,
                        sleep_time: float):
        """
            Flying movement with the addiction of a time interval
        """

        super().send_rc_control(left_right_velocity,
                                forward_backward_velocity,
                                yaw_velocity,
                                up_down_velocity)
        if sleep_time > 0:
            sleep(sleep_time)

        self.logger.debug("Movement ->",
                          f'left_right:{left_right_velocity}',
                          f'forward_backward:{forward_backward_velocity}',
                          f'yaw:{yaw_velocity}',
                          f'up_down:{up_down_velocity}',
                          f'sleep:{sleep_time}')

    def takeoff(self):
        """
            Start Take-Off with the addiction of a waiting interval of 2 secs.
            In this way, the drone will takes-off avoiding unwanted movements
        """

        self.logger.info('Starting Take-Off')

        super().takeoff()
        self.send_rc_control(0, 0, 0, 0, 2)

        self.logger.info("Take-Off completed")

    def land(self):
        """
            Start landing with the addiction of a waiting interval of 2 secs.
            In this way, the drone will land avoiding unwanted movements
        """

        self.logger.info('Starting Landing')

        self.send_rc_control(0, 0, 0, 0, 2)
        super().land()

        self.logger.info('Landing completed')

    def start_streaming(self):
        if not self.stream_on:
            self.streamon()
            self.logger.info('Streaming: ON')
        else:
            self.logger.warning('Streaming already ON')

    def stop_streaming(self):
        if self.stream_on:
            self.streamoff()
            self.logger.info('Streaming: OFF')
        else:
            self.logger.warning('Streaming already OFF')

    def get_img(self, resize_x: int, resize_y: int):
        """
            Returns the frame captured by tello.
            If resize params are given, the image will be resized
            for example 720 x 480.
            If zero is passed, it will use the half of resolution of your screen

        """
        width = GetSystemMetrics(0) / 2
        height = GetSystemMetrics(1) / 2

        if resize_x != 0:
            width = resize_x

        if resize_y != 0:
            height = resize_y

        img = self.get_frame_read().frame
        img = cv2.resize(img, (width, height))
        cv2.imshow("Tello Image", img)
        cv2.waitKey(1)

        return img

    def save_img(self, img: BackgroundFrameRead):
        img_name = f'\\{time.time()}.jpg'
        out_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        out_path = out_path + '\\TelloCaptures'
        if not os.path.isdir(out_path):
            os.makedirs(out_path)

        out_path = out_path + img_name

        cv2.imwrite(out_path, img.frame)
        time.sleep(0.3)
        self.logger.info("frame captured:", out_path)
