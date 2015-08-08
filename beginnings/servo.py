import time
import numpy as np
import RPi.GPIO as gpio

gpio.setmode(gpio.BOARD)
gpio.setup(11, gpio.OUT)

pwm = gpio.PWM(11, 50)

pwm.start(1)

time.sleep(1)

for i in np.arange(1, 14, 0.5):
    pwm.ChangeDutyCycle(i)
    time.sleep(1)

pwm.stop()
gpio.cleanup()
