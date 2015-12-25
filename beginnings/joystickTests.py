import time
import pygame

class Button:
    A = 0 # Triangle
    B = 1 # O
    X = 2 # X
    Y = 3 # Square
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
forearmPos = 90
gripperPos = 10

# Initialize joystick
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
print 'Joystick initalized, press A to exit'

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

    time.sleep(0.5)

    # Display all button events
    print [(button(i), button(i)) for i in xrange(joystick.get_numbuttons())]
    # print [axis(i) for i in xrange(joystick.get_numaxes())]
    # print [hat(i) for i in xrange(joystick.get_numhats())]

    done = button(Button.RBumper)
    baseChange = False
    armChange = False
    forearmChange = False
    gripperChange = False

    if axis(Axis.RThumbX) >= 0.1 and basePos < 175:
        basePos += axis(Axis.RThumbX)*5
    if axis(Axis.RThumbX) <= -0.1 and basePos > 5:
        basePos += axis(Axis.RThumbX)*5

    if axis(Axis.RThumbY) >= 0.1 and armPos < 175:
        armPos += axis(Axis.RThumbY)*5
    if axis(Axis.RThumbY) <= -0.1 and armPos > 5:
        armPos += axis(Axis.RThumbY)*5

    if axis(Axis.LThumbY) >= 0.1 and forearmPos < 175:
        forearmPos += axis(Axis.LThumbY)*5
    if axis(Axis.LThumbY) <= -0.1 and forearmPos > 5:
        forearmPos += axis(Axis.LThumbY)*5

    if button(Button.X) and gripperPos < 70:
        gripperPos += 1
    elif button(Button.B) and gripperPos > 25:
        gripperPos -= 1

# Quit joystick control
joystick.quit()
pygame.joystick.quit()
pygame.quit()
