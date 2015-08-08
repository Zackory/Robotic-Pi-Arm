import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup(2, gpio.IN, pull_up_down=gpio.PUD_UP)

isPressed = False
while True:
    if gpio.input(2) == gpio.LOW and not isPressed:
        print 'Switch pressed'
        isPressed = True
    elif gpio.input(2) == gpio.HIGH and isPressed:
        print 'Switch released'
        isPressed = False

gpio.cleanup()
