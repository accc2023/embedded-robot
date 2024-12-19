import RPi.GPIO as GPIO
import time

# GPIO Pin assignments
s0 = 2
s1 = 3
s2 = 23
s3 = 24
signal = 25
NUM_CYCLES = 10
mins = [10**9]*3
maxs = [-1]*3

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(signal, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup([s0, s1, s2, s3], GPIO.OUT)
    
    # Set frequency scaling to 100% (High-High)
    GPIO.output(s0, GPIO.LOW)
    GPIO.output(s1, GPIO.HIGH)
    print("Setup complete with frequency scaling set to 2%.\n")

def read_color():
    # Read Red
    GPIO.output(s2, GPIO.LOW)
    GPIO.output(s3, GPIO.LOW)
    time.sleep(0.3)
    red = read_frequency()

    # Read Green
    GPIO.output(s2, GPIO.HIGH)
    GPIO.output(s3, GPIO.HIGH)
    time.sleep(0.3)
    green = read_frequency()

    # Read Blue
    GPIO.output(s2, GPIO.LOW)
    GPIO.output(s3, GPIO.HIGH)
    time.sleep(0.3)
    blue = read_frequency()

    return red, green, blue

def read_frequency():
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
        GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start
    return NUM_CYCLES / duration

fD_big = 1200
fW_big = 37000
fD_2 =8500
fW_2 =22000

def convert_frequency_to_rgb(fO, fD=1100, fW=3350):
    if fO < fD:  # In case of noise that might result in lower than dark frequency
        return 0
    elif fO > fW:  # In case of noise that might result in higher than white frequency
        return 255
    else:
        return int(255 * (fO - fD) / (fW - fD))

def loop():
    while True:
        red, green, blue = read_color()
        l = [red, green, blue]
        for i in range(3):
            maxs[i] = max(l[i], maxs[i])
            mins[i] = min(l[i], mins[i])
        #print(f"Red: {convert_frequency_to_rgb(red)}, Green: {convert_frequency_to_rgb(green)}, Blue: {convert_frequency_to_rgb(blue)}")
        print(f"Red: {red}, Green: {green}, Blue: {blue}")

def end_program():
    print("Max values:", *maxs)
    print("Min values:", *mins)
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        end_program()