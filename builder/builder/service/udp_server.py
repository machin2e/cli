from socket import *

def server():
	PORT = 4445

	serverSocket = socket(AF_INET, SOCK_DGRAM)
	serverSocket.bind(('', PORT))

	response_timeout = 2.0 # seconds

	#serverSocket.settimeout(response_timeout)
	serverSocket.setblocking(0)

	configuration = {}

	while True:
		try:
			message, address = serverSocket.recvfrom(1024)
			# print message, address

			if message.startswith("announce"):
				print "Received:", message, "from", address

			elif message.startswith("configure"):
				# e.g., "configuration key:value"
				data = message[len("configure") + 1:] # remove "echo " from start of string
				pair = data.split(':')
				key = pair[0]
				value = pair[1]
				configuration[key] = value
				response_message = "key: %s, value: %s" % (key, configuration[key])
				serverSocket.sendto(response_message, address)

				# Update configuration file on disk
				# TODO: Just update the in-memory and sync to disc periodically
				builderfile_path = 'fooBuilderfile'

				# Create default Builderfile if it doesn't exist.
				#if not os.path.exists(builderfile_path):
				file = open(builderfile_path, 'w')

				# Write entry in dictionary
				for key in configuration:
					file.write("%s:%s\n" % (key, configuration[key]))

				file.close()

			elif message.startswith("echo"):
				response_message = message[len("echo") + 1:] # remove "echo " from start of string
				print response_message
				serverSocket.sendto(response_message, address)

		except:
			None

	serverSocket.close()

if __name__ == "__main__":
	server()
