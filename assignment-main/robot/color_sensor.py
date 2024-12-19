from enum import Enum
from robot import (SIGNAL_SENSOR_PIN, 
                   COLOR_SENSOR_PIN_1, 
                   COLOR_SENSOR_PIN_2, 
                   COLOR_SENSOR_PIN_3, 
                   COLOR_SENSOR_PIN_4)
import RPi.GPIO as GPIO
import time


class Color(Enum):
    OTHER = 1
    BLACK = 2
    WHITE = 3


class ColorSensor:

    NUM_CYCLES = 10
    SCANNING_CYCLES = 50
    LOWER_BLACK = 100
    HIGHER_WHITE = 400
    DARK_FREQUENCY = 1100
    WHITE_FREQUENCY = 3350

    def __init__(self):
        ColorSensor.setup()


    def detectColor(self) -> Color:
        red_avg = 0
        green_avg = 0
        blue_avg = 0
        for _ in range(self.SCANNING_CYCLES):
            red, green, blue = self.read_color()
            red_avg += red
            green_avg += green
            blue_avg += blue
        red_avg /= self.SCANNING_CYCLES
        green_avg /= self.SCANNING_CYCLES
        blue_avg /= self.SCANNING_CYCLES

        red_avg_rgb = self.convert_frequency_to_rgb(red_avg)
        green_avg_rgb = self.convert_frequency_to_rgb(green_avg)
        blue_avg_rgb = self.convert_frequency_to_rgb(blue_avg)

        if red_avg_rgb < self.LOWER_BLACK and green_avg_rgb < self.LOWER_BLACK and blue_avg_rgb < self.LOWER_BLACK:
            color = Color.BLACK
        elif red_avg_rgb > self.HIGHER_WHITE and green_avg_rgb > self.HIGHER_WHITE and blue_avg_rgb > self.HIGHER_WHITE:
            color = Color.WHITE
        else:
            color = Color.OTHER

        return color
        

    @staticmethod     
    def setup():
        GPIO.setup(SIGNAL_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup([COLOR_SENSOR_PIN_1, COLOR_SENSOR_PIN_2, COLOR_SENSOR_PIN_3, COLOR_SENSOR_PIN_4], GPIO.OUT)
        
        # Set frequency scaling to 100% (High-High)
        GPIO.output(COLOR_SENSOR_PIN_1, GPIO.LOW)
        GPIO.output(COLOR_SENSOR_PIN_2, GPIO.HIGH)


    def read_color(self):
        # Read Red
        GPIO.output(COLOR_SENSOR_PIN_3, GPIO.LOW)
        GPIO.output(COLOR_SENSOR_PIN_4, GPIO.LOW)
        time.sleep(0.3)
        red = self.read_frequency()

        GPIO.output(COLOR_SENSOR_PIN_3, GPIO.HIGH)
        GPIO.output(COLOR_SENSOR_PIN_4, GPIO.HIGH)
        time.sleep(0.3)
        green = self.read_frequency()

        # Read Blue
        GPIO.output(COLOR_SENSOR_PIN_3, GPIO.LOW)
        GPIO.output(COLOR_SENSOR_PIN_4, GPIO.HIGH)
        time.sleep(0.3)
        blue = self.read_frequency()

        return red, green, blue
    

    def read_frequency(self):
        start = time.time()
        for impulse_count in range(self.NUM_CYCLES):
            GPIO.wait_for_edge(SIGNAL_SENSOR_PIN, GPIO.FALLING)
        duration = time.time() - start
        return self.NUM_CYCLES / duration
    

    def convert_frequency_to_rgb(self, frequency_to_convert):
        if frequency_to_convert < self.DARK_FREQUENCY:  # In case of noise that might result in lower than dark frequency
            return 0
        elif frequency_to_convert > self.WHITE_FREQUENCY:  # In case of noise that might result in higher than white frequency
            return 255
        else:
            return int(255 * (frequency_to_convert - self.DARK_FREQUENCY) / (self.WHITE_FREQUENCY - self.DARK_FREQUENCY))
        