import time
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup(2, gpio.OUT)

while True:
    gpio.output(2, gpio.HIGH)
    time.sleep(1)
    gpio.output(2, gpio.LOW)
    time.sleep(1)
