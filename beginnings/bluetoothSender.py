import sys
import bluetooth

uuid = '3cec75d6-81f6-496a-86e6-4455c2a75981'
serviceMatches = bluetooth.find_service(uuid=uuid)

if len(serviceMatches) == 0:
    print 'Could not find the arm launcher'
    sys.exit(0)

firstMatch = serviceMatches[0]
port = firstMatch['port']
name = firstMatch['name']
host = firstMatch['host']

print 'Connecting to \'%s\' on %s' % (name, host)

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((host, port))
sock.send('Hello!')
sock.close()
