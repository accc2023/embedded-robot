from shield_manager import ShieldManager
from robot import CONVEYOR_MOTOR

class Conveyor:
    def __init__(self):
        self.shieldManager: ShieldManager = ShieldManager.getInstance()
        self.motor = CONVEYOR_MOTOR

    def move(self, forward: bool =True, speed: int = 100) -> bool:
        return self.shieldManager.runMotor(self.motor, forward, speed)

    def stop(self) -> bool:
        return self.shieldManager.stopMotor(self.motor)