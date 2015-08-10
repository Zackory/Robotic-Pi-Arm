import lightblue
import RPi.GPIO as gpio

def createPWMs(ports):
    for i in ports:
        gpio.setup(i, gpio.OUT)
    # Setup pwm ports using 50 Hz
    return [gpio.PWM(i, 50) for i in ports]

gpio.setmode(gpio.BOARD)
base, arm, forearm, gripper = createPWMs([11, 12, 15, 16])

# Start servos at center point (90 degrees)
# Min 2.5 (0 degrees), Max 12.5 (180 degrees)
base.start(7.5)
arm.start(7.5)
forearm.start(7.5)
gripper.start(7.5)

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
    basePos, armPos, forearmPos, gripperPos = data.split(',')
    # base.ChangeDutyCycle(basePos)
    # arm.ChangeDutyCycle(armPos)
    # forearm.ChangeDutyCycle(forearmPos)
    # gripper.ChangeDutyCycle(gripperPos)
    print 'Received [%s]' % data

# Close bluetooth
connection.close()
s.close()

# Stop servos
base.stop()
arm.stop()
forearm.stop()
gripper.stop()
gpio.cleanup()
