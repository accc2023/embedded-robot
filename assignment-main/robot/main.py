import RPi.GPIO as GPIO
from robot import Robot, SIGNAL


def setup() -> None:
    """
    Setup environment for robot.
    """
    
    GPIO.setmode(GPIO.BCM)


if __name__ == "__main__":
    setup()
    robot = Robot()
    robot.run()
