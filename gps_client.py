import socket
import serial
import pynmea2
import time
def parseGPS(s_port, s):
	str = s_port.readline()
#	s.send(str.encode(encoding='utf_8', errors = 'strict'))
#	data = s.recv(1024)
#	print 'result: ' + (data.decode())
	if str.find('GGA')>0:
		print str
		msg = pynmea2.parse(str)
		print "Lat: %s %s -- Lon: %s %s" %(msg.lat, msg.lat_dir, msg.lon, msg.lon_dir)
		msg = msg.lat + "," + msg.lon 
		print "msg : " + msg
		s.send(msg.encode(encoding='utf_8',errors = 'strict'))
		print "receving data........."
		data = s.recv(1024)
		print 'result: ' + (data.decode())
	else:
		msg = "GPS is not working"
		print msg
		s.send(msg.encode(encoding='utf_8', errors = 'strict'))
		print "receving data........"
		data = s.recv(1024)
		print 'result: ' + (data.decode())
		
HOST = 'IP ADD'
PORT = "PORT NUM"

serialPort = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
	#s.connect((HOST, PORT))
	#str = serialPort.readline()
	parseGPS(serialPort, s)
	time.sleep(0.5)

s.close()
