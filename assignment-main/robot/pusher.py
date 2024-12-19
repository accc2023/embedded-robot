from time import sleep

from shield_manager import ShieldManager
from robot import PUSHER_MOTOR

class Pusher:
    ROTATION_TIME = 0.04 #???? Need to experiment
    WAIT_TIME = 0.1 #???? Need to experiment
    
    def __init__(self):
        self.shieldManager = ShieldManager.getInstance()
        self.motor = PUSHER_MOTOR
        
    def push_right(self):
        self.rotate_motor(False)
        sleep(self.WAIT_TIME)
        self.rotate_motor(True)
    
    def push_left(self):
        self.rotate_motor(True)
        sleep(self.WAIT_TIME)
        self.rotate_motor(False)
    
    def rotate_motor(self, left: bool):
        self.shieldManager.runMotor(self.motor, left)
        sleep(self.ROTATION_TIME)
        self.shieldManager.stopMotor(self.motor)
        