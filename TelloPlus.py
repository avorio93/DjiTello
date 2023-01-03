from djitellopy import tello
from time import sleep
from multipledispatch import dispatch
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
    LOG_NAME = 'TELLO_EXT'

    # ---> Attributes

    ####################################################################################################################
    # CORE

    # ---> Functions
    @dispatch(tello.Tello, int, int, int, int, float)
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

        self.logger.debug('Movement ->',
                          f'left_right:{left_right_velocity}',
                          f'forward_backward:{forward_backward_velocity}',
                          f'yaw:{yaw_velocity}',
                          f'up_down:{up_down_velocity}',
                          f'sleep:{sleep_time}')

    def takeoff(self):
        """
            Start take-off with the addiction of a waiting interval of 2 secs.
            In this way, the drone will takes-off avoiding unwanted movements
        """

        self.logger.info('Starting Take-Off')

        super().takeoff()
        self.send_rc_control(0, 0, 0, 0, 2)

        self.logger.info('Take-Off completed')

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
            Returns the frame captured by tello resized
        """

        # TODO
        width = GetSystemMetrics(0) / 2
        height = GetSystemMetrics(1) / 2

        if resize_x != 0:
            width = resize_x

        if resize_y != 0:
            height = resize_y

        img = self.get_frame_read().frame
        img = cv2.resize(img, (width, height))
        # cv2.imshow("Tello Image", img)
        cv2.waitKey(1)
        return img

    # ---> Constructor
    def __init__(self):

        # Logger init
        self.logger = CustomLogger(self.LOG_NAME, write_file=False).logger
        self.logger.info('Connection init...')

        # Create a Tello instance and connect it to the drone
        super().__init__()
        self.connect()

        if self.get_battery() > 0:
            self.logger.info('Successfully connected!')
        else:
            self.logger.error('Connection refused')
            raise Exception()

        # Check if drone is ready to take-off
        self.logger.info('Battery Level:' + str(self.get_battery()))
        if self.get_battery() >= TelloPlus.CRITICAL_BATTERY:
            self.logger.info('Ready to fly!')

        else:
            self.logger.critical('Low battery level: unable to take off')
            raise Exception()
