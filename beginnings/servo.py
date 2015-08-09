import time
import numpy as np
import RPi.GPIO as gpio

gpio.setmode(gpio.BOARD)
gpio.setup(11, gpio.OUT)

pwm = gpio.PWM(11, 50)

pwm.start(2.5)

time.sleep(1)

# Min 2, Max 12.5
for i in np.arange(1.5, 14, 0.5):
    print i
    pwm.ChangeDutyCycle(i)
    time.sleep(1)

pwm.stop()
gpio.cleanup()
