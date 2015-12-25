__author__ = 'zackory'

import time
import pygame
import pigpio

class Button:
    A = 0
    B = 1
    X = 2
    Y = 3
    LBumper = 4
    RBumper = 5

class Axis:
    LThumbX = 0
    LThumbY = 1
    LTrigger = 2
    RThumbX = 3
    RThumbY = 4
    RTrigger = 5

# Initialize servo positions
done = False
basePos = 1500 # 1000 low, 2000 high
armPos = 1500 # 1000 low, 2000 high
forearmPos = 1400 # 1000 low, 2000 high
gripperPos = 750 # 700 low, 1000 high

# Initialize joystick
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
print 'Joystick initalized, press A to exit'

# Fix error of triggers not appearing as axes
if joystick.get_numaxes() < 6:
    class Button:
        A = 0 # Triangle
        B = 1 # O
        X = 2 # X
        Y = 3 # Square
        LBumper = 4
        RBumper = 5
        LTrigger = 6
        RTrigger = 7

    class Axis:
        LThumbX = 0
        LThumbY = 1
        RThumbX = 2
        RThumbY = 3
        Unknown = 4

gpio = pigpio.pi()

base, arm, forearm, gripper = [17, 18, 22, 23]

# Start servos at center points
gpio.set_servo_pulsewidth(base, basePos)
gpio.set_servo_pulsewidth(arm, armPos)
gpio.set_servo_pulsewidth(forearm, forearmPos)
gpio.set_servo_pulsewidth(gripper, gripperPos)

# Helper functions
def button(i):
    return joystick.get_button(i) == 1
def axis(i):
    return joystick.get_axis(i)
def hat(i):
    return joystick.get_hat(i)

# Main loop
while not done:
    # Process all events from pygame
    for event in pygame.event.get():
        pass

    # Display all button events
    # print [(button(i), button(i)) for i in xrange(joystick.get_numbuttons())]
    # print [axis(i) for i in xrange(joystick.get_numaxes())]
    # print [hat(i) for i in xrange(joystick.get_numhats())]

    done = button(Button.RBumper)
    baseChange = False
    armChange = False
    forearmChange = False
    gripperChange = False

    mag = 30

    if (axis(Axis.RThumbX) <= -0.1 and basePos < 2000 - mag) or \
            (axis(Axis.RThumbX) >= 0.1 and basePos > 1000 + mag):
        basePos -= axis(Axis.RThumbX)*mag
        baseChange = True

    if (axis(Axis.RThumbY) >= 0.1 and armPos < 2000 - mag) or \
            (axis(Axis.RThumbY) <= -0.1 and armPos > 1000 + mag):
        armPos += axis(Axis.RThumbY)*mag
        armChange = True

    if (axis(Axis.LThumbY) <= -0.1 and forearmPos < 2000 - mag) or \
            (axis(Axis.LThumbY) >= 0.1 and forearmPos > 1000 + mag):
        forearmPos -= axis(Axis.LThumbY)*mag
        forearmChange = True

    if (axis(Axis.LThumbX) >= 0.1 and gripperPos < 1000 - mag) or \
            (axis(Axis.LThumbX) <= -0.1 and gripperPos > 700 + mag):
        gripperPos += axis(Axis.LThumbX)*mag
        gripperChange = True

    print 'BasePos:', basePos, 'armPos:', armPos, 'forearmPos:', forearmPos, 'gripperPos:', gripperPos

    # Update servo positions
    if baseChange:
        gpio.set_servo_pulsewidth(base, basePos)
    if armChange:
        gpio.set_servo_pulsewidth(arm, armPos)
    if forearmChange:
        gpio.set_servo_pulsewidth(forearm, forearmPos)
    if gripperChange:
        gpio.set_servo_pulsewidth(gripper, gripperPos)

    # Wait a little
    time.sleep(0.05)

# Quit joystick control
joystick.quit()
pygame.joystick.quit()
pygame.quit()

# Stop servos
gpio.set_servo_pulsewidth(base, 0)
gpio.set_servo_pulsewidth(arm, 0)
gpio.set_servo_pulsewidth(forearm, 0)
gpio.set_servo_pulsewidth(gripper, 0)
gpio.stop()
