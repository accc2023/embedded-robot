import time
from conveyor import Conveyor
from color_sensor import ColorSensor, Color
from motion_sensor import MotionSensor, MotionState
from pusher import Pusher

class Robot:
    def __init__(self):
        self.conveyor = Conveyor()
        self.pusher = Pusher()
        self.color_sensor = ColorSensor()
        self.motion_sensor = MotionSensor()

    def run(self):
        self.conveyor.move()

        try:
            while True:
                if not self.motion_sensor.detectObject():
                    time.sleep(0.2)
                    continue
                color: Color = self.sensor.detectColor()
                match color:
                    case Color.BLACK:
                        self.pusher.push_left()
                    case Color.WHITE:
                        self.pusher.push_right()
                    case _:
                        pass
                time.sleep(0.2)
        finally:
            self.conveyor.stop()