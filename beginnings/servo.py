import time
import numpy as np
import RPi.GPIO as gpio

gpio.setmode(gpio.BOARD)
gpio.setup(11, gpio.OUT)

pwm = gpio.PWM(11, 50)

pwm.start(7.5)

time.sleep(1)

for i in np.arange(2.5, 13, 0.5):
    pwm.ChangeDutyCycle(i)
    time.sleep(0.5)

pwm.stop()
gpio.cleanup()
