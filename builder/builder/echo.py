# Send UDP broadcast packets
import sys, time
import socket
import uuid

def echo(message):
	PORT = 4445

	device_uuid = uuid.uuid4()
	#print "uuid: %s" % uuid

	broadcast_address = '192.168.1.255' # '<broadcast>'

	response_timeout = 2.0 # seconds

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('', 0))
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

	# s.settimeout(response_timeout)
	s.setblocking(0)

	data = "echo %s" % message
	s.sendto(data, (broadcast_address, PORT)) # Works

	response_start_time = int(round(time.time() * 1000))
	current_time = 0
	timeout = 2500

	while current_time - response_start_time < timeout:
		try:
			data, fromaddr = s.recvfrom(1000)
			print "Response from %s:%s: %s" % (fromaddr[0], fromaddr[1], data)
		except:
			None
		current_time = int(round(time.time() * 1000))
	s.close()

if __name__ == "__main__":
	echo("hello")
