import time

# Check if running on Raspberry Pi
try:
    import RPi.GPIO as GPIO

    PI = True

    LEFT_PIN = 17
    RIGHT_PIN = 27

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(LEFT_PIN, GPIO.OUT)
    GPIO.setup(RIGHT_PIN, GPIO.OUT)

except ImportError:

    PI = False


def vibrate_left():

    if PI:
        GPIO.output(LEFT_PIN, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(LEFT_PIN, GPIO.LOW)
    else:
        print("<< LEFT VIBRATION >>")


def vibrate_right():

    if PI:
        GPIO.output(RIGHT_PIN, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(RIGHT_PIN, GPIO.LOW)
    else:
        print("<< RIGHT VIBRATION >>")


def vibrate_both():

    if PI:

        GPIO.output(LEFT_PIN, GPIO.HIGH)
        GPIO.output(RIGHT_PIN, GPIO.HIGH)

        time.sleep(0.3)

        GPIO.output(LEFT_PIN, GPIO.LOW)
        GPIO.output(RIGHT_PIN, GPIO.LOW)

    else:
        print("<< BOTH VIBRATION >>")


def cleanup():

    if PI:
        GPIO.cleanup()