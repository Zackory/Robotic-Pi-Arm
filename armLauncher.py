__author__ = 'zackory'

import lightblue
import RPi.GPIO as gpio

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

gpio.setmode(gpio.BOARD)
base, arm, forearm, gripper = createPWMs([11, 12, 15, 16])

# Start servos at center point (90 degrees)
base.start(angleToPos(90))
arm.start(angleToPos(90))
forearm.start(angleToPos(90))
gripper.start(angleToPos(10))

# Initialize bluetooth on a specific port
port = 5
s = lightblue.socket()
s.bind(('', port))
s.listen(1)
print 'Listening on port', port

# Advertise bluetooth connection and wait for connection
lightblue.advertise('Arm Launcher', s, lightblue.RFCOMM)
connection, address = s.accept()
print 'Accepted connection from', address

while True:
    data = connection.recv(1024)
    if data == 'Done':
        print 'Done command received'
        break
    try:
        baseAngle, armAngle, forearmAngle, gripperAngle = (float(angle) for angle in data.split(','))
    except:
        continue
    base.ChangeDutyCycle(angleToPos(baseAngle))
    arm.ChangeDutyCycle(angleToPos(armAngle))
    forearm.ChangeDutyCycle(angleToPos(forearmAngle))
    gripper.ChangeDutyCycle(angleToPos(gripperAngle))
    # print 'Received [%s]' % data

# Close bluetooth
connection.close()
s.close()

# Stop servos
base.stop()
arm.stop()
forearm.stop()
gripper.stop()
gpio.cleanup()
