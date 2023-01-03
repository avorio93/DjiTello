from djitellopy import tello
from time import sleep
from CustomLogger import CustomLogger
import cv2  # If not working, add the path manually to the interpreter


class MyTello(tello.Tello):
    # Constants Declarations
    CRITICAL_BATTERY = 15

    # Attributes Declarations
    LOG_NAME = 'MY_TELLO'

    def __init__(self):

        self.logger = CustomLogger(self.LOG_NAME).logger
        self.logger.info('Connection init...')

        # Create a Tello instance and connect it to the drone
        super().__init__()
        # self.LOGGER.setLevel(logging.CRITICAL)
        self.connect()

        if self.get_battery() > 0:
            self.logger.info('Successfully connected!')
        else:
            self.logger.error('Connection refused')
            raise Exception()

        # Check if drone is ready to take off
        self.logger.info('Battery Level:' + str(self.get_battery()))
        if self.get_battery() >= MyTello.CRITICAL_BATTERY:
            self.logger.info('Ready to fly!')

        else:
            self.logger.critical('Low battery level: unable to take off')
            raise Exception()

    def send_rc_control(self,
                        left_right_velocity: int,
                        forward_backward_velocity: int,
                        up_down_velocity: int,
                        yaw_velocity: int,
                        sleep_time: float):

        # Start flying movement and wait
        super().send_rc_control(left_right_velocity,
                                forward_backward_velocity,
                                yaw_velocity,
                                up_down_velocity)

        sleep(sleep_time)

    def takeoff(self):
        self.logger.info('Starting Take-Off')

        super().takeoff()
        self.send_rc_control(0, 0, 0, 0, 2)

        self.logger.info('Take-Off completed')

    def land(self):
        self.logger.info('Starting Landing')

        self.send_rc_control(0, 0, 0, 0, 2)
        super().land()

        self.logger.info('Landing completed')

    def start_streaming(self):
        self.streamon()
        self.logger.info('Streaming: ON')

        """""
        while True:
            img = self.get_frame_read().frame
            img = cv2.resize(img, (360, 240))
            cv2.imshow("Tello Image", img)
            cv2.waitKey(1)
        """""

    def stop_streaming(self):
        self.streamoff()
        self.logger.info('Streaming: OFF')
