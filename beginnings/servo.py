import time
import numpy as np
import RPi.GPIO as gpio

gpio.setmode(gpio.BOARD)
gpio.setup(11, gpio.OUT)

pwm = gpio.PWM(11, 50)

# Start at center point (90 degrees)
pwm.start(7.5)

time.sleep(1)

# Min 2.5 (0 degrees), Max 12.5 (180 degrees)
for i in np.arange(2.5, 13, 0.5):
    print i
    pwm.ChangeDutyCycle(i)
    time.sleep(1)

pwm.stop()
gpio.cleanup()
