import lightblue

s = lightblue.socket()
s.connect(('00:0A:3A:84:1F:A6', 1))
s.send('Hello!')
s.close()
