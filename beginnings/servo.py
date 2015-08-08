import time
import RPi.GPIO as gpio

gpio.setmode(gpio.BOARD)
gpio.setup(11, gpio.OUT)

pwm = gpio.PWM(11, 50)

pwm.start(10)

for i in xrange(10, 100, 10):
    pwm.ChangeDutyCycle(i)
    time.sleep(0.5)

pwm.stop()
gpio.cleanup()
