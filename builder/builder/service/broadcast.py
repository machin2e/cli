# Send UDP broadcast packets
import sys, time
import socket
import uuid

def start():
	None

def stop():
	None

def run(port=4445, broadcast_address='192.168.1.255', broadcast_period=2):

	device_uuid = uuid.uuid4()

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('', 0))
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

	# "\f<content_length>\t<content_checksum>\t<content_type>\t<content>"
	# e.g., "\f52	16561	text	announce device 002fffff-ffff-ffff-4e45-3158200a0015"
	# data = "\f52\t16561\ttext\tannounce device 002fffff-ffff-ffff-4e45-3158200a0015";
	# data = "\f52\t33439\ttext\tannounce device f1aceb8b-e8e9-4cda-b29c-de7bc7cc390f"
	message = "announce device %s" % device_uuid

	while 1:
	    s.sendto(message, (broadcast_address, port)) # Works
	    time.sleep(broadcast_period)

if __name__ == "__main__":
	run()
