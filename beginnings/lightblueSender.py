import lightblue

s = lightblue.socket()
s.connect(('00:0A:3A:84:1F:A6', 5))
s.send('Hello!')
s.close()

# import bluetooth
# from pprint import pprint
# serviceMatches = bluetooth.find_service(address='00:0A:3A:84:1F:A6')
# pprint(serviceMatches)
