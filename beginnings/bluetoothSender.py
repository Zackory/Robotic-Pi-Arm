import sys
import bluetooth

serviceMatches = bluetooth.find_service(address='00:0A:3A:84:1F:A6')

if len(serviceMatches) == 0:
    print 'Could not find the arm launcher'
    sys.exit(0)

firstMatch = serviceMatches[6]
port = firstMatch['port']
name = firstMatch['name']
host = firstMatch['host']

print 'Connecting to \'%s\' on %s, port: %s' % (name, host, port)

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((host, port))
sock.send('Hello!')
sock.close()
