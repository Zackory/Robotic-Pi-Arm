import pygame
import RPi.GPIO as gpio

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

def createPWMs(ports, hz=100):
    for i in ports:
        gpio.setup(i, gpio.OUT)
    # Setup pwm ports using specified Hz
    return [gpio.PWM(i, hz) for i in ports]

def angleToPos(angle, hz=100):
    # For 50 Hz: Min 2.5 (0 degrees), Max 12.5 (180 degrees)
    # For 100 Hz: Min 5 (0 degrees), Max 26 (180 degrees)
    scale = (hz - 50.0) / 50.0 + 1.0
    return (angle / 180.0 * 10.0 + 2.5) * scale

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

gpio.setmode(gpio.BOARD)
base, arm, forearm, gripper = createPWMs([11, 12, 15, 16])

# Start servos at center point (90 degrees)
base.start(angleToPos(basePos))
arm.start(angleToPos(armPos))
forearm.start(angleToPos(forearmPos))
gripper.start(angleToPos(gripperPos))

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

    if button(Button.X) and gripperPos < 70:
        gripperPos += 1
        gripperChange = True
    elif button(Button.B) and gripperPos > 25:
        gripperPos -= 1
        gripperChange = True

    print 'BasePos:', basePos, 'armPos:', armPos, 'forearmPos:', forearmPos, 'gripperPos:', gripperPos

    # Update servo positions
    if baseChange:
        base.ChangeDutyCycle(angleToPos(basePos))
    if armChange:
        arm.ChangeDutyCycle(angleToPos(armPos))
    if forearmChange:
        forearm.ChangeDutyCycle(angleToPos(forearmPos))
    if gripperChange:
        gripper.ChangeDutyCycle(angleToPos(gripperPos))

# Quit joystick control
joystick.quit()
pygame.joystick.quit()
pygame.quit()

# Stop servos
base.stop()
arm.stop()
forearm.stop()
gripper.stop()
gpio.cleanup()
