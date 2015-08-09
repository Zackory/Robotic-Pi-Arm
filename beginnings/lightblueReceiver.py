import lightblue

port = 1
s = lightblue.socket()
s.bind(('', port))
s.listen(1)
print 'Listening on port', port
lightblue.advertise('Arm Launcher', s, lightblue.RFCOMM)
connection, address = s.accept()
print 'Accepted connection from', address

while True:
    data = connection.recv(1024)
    if not data:
        break
    print 'Received [%s]' % data

connection.close()
s.close()
