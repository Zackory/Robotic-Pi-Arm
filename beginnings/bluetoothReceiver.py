import bluetooth

serverSock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# port = bluetooth.get_available_port(bluetooth.RFCOMM)
port = 1
serverSock.bind(('', port))
serverSock.listen(1)
print 'Listening on port', port

uuid = '3cec75d6-81f6-496a-86e6-4455c2a75981'
bluetooth.advertise_service(serverSock, 'Arm Launcher', uuid)

sock, address = serverSock.accept()
print 'Accepted connection from', address

while True:
    data = sock.recv(1024)
    if not data:
        print 'No data'
        continue
    print 'Received [%s]' % data

sock.close()
serverSock.close()
