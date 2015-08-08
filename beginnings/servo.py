import RPi.GPIO as gpio

gpio.setmode(gpio.BOARD)
gpio.setup(11, gpio.out)

pwm = gpio.PWM(11, 50)

pwm.start(10)

for i in xrange(10, 100, 10):
    pwm.ChangeDutyCycle(i)

pwm.stop()
gpio.cleanup()
