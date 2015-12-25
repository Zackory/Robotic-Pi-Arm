import os
import time
import pygame

def pwm(pin, angle):
    # Angle between 0 and 250
    # print "servo[" + str(pin) + "][" + str(angle) + "]"
    cmd = "echo " + str(pin) + "=" + str(angle) + " > /dev/servoblaster"
    os.system(cmd)

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
basePos = 90
armPos = 90
forearmPos = 75
gripperPos = 10

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

# gpio.setmode(gpio.BOARD)
# base, arm, forearm, gripper = createPWMs([11, 12, 15, 16])
base, arm, forearm, gripper = [11, 12, 15, 16]

# Start servos at center points
pwm(base, basePos)
pwm(arm, armPos)
pwm(forearm, forearmPos)
pwm(gripper, gripperPos)

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

    if axis(Axis.RThumbX) >= 0.1 and basePos < 175:
        basePos += axis(Axis.RThumbX)*5
        baseChange = True
    if axis(Axis.RThumbX) <= -0.1 and basePos > 5:
        basePos += axis(Axis.RThumbX)*5
        baseChange = True

    if axis(Axis.RThumbY) >= 0.1 and armPos < 175:
        armPos += axis(Axis.RThumbY)*5
        armChange = True
    if axis(Axis.RThumbY) <= -0.1 and armPos > 5:
        armPos += axis(Axis.RThumbY)*5
        armChange = True

    if axis(Axis.LThumbY) >= 0.1 and forearmPos < 175:
        forearmPos += axis(Axis.LThumbY)*5
        forearmChange = True
    if axis(Axis.LThumbY) <= -0.1 and forearmPos > 5:
        forearmPos += axis(Axis.LThumbY)*5
        forearmChange = True

    if button(Button.X) and gripperPos < 40:
        gripperPos += 1
        gripperChange = True
    elif button(Button.B) and gripperPos > 10:
        gripperPos -= 1
        gripperChange = True

    print 'BasePos:', basePos, 'armPos:', armPos, 'forearmPos:', forearmPos, 'gripperPos:', gripperPos

    # Update servo positions
    if baseChange:
        pwm(base, basePos)
    if armChange:
        pwm(arm, armPos)
    if forearmChange:
        pwm(forearm, forearmPos)
    if gripperChange:
        pwm(gripper, gripperPos)

    # Wait a little
    time.sleep(0.05)

# Quit joystick control
joystick.quit()
pygame.joystick.quit()
pygame.quit()

# Stop servos
base.stop()
arm.stop()
forearm.stop()
gripper.stop()
