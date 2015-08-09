import lightblue

s = lightblue.socket()
s.connect(('C0:18:85:EB:3D:9D', 5))
s.send('Hello!')
s.close()
