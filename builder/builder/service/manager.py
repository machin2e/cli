import os, sys
import subprocess, psutil, tempfile, portalocker
import json
import socket
import logging
from ..util import util

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import urlparse
import cgi

# Initialize logging
logger = util.setup_log_folder(__name__)

def start():
	sys.stdout.write('Starting manager service.')

	current_dir = os.getcwdu()
	p = subprocess.Popen(['builder', 'run', 'manager'], cwd=current_dir)
	sys.stdout.write(' OK.\n')

	# Log status
	logger.info('Started manager service.')

def stop():
	sys.stdout.write('Stopping manager service.')

	# Log status
	logger.info('Stopped manager service.')

	# Locate pidfile (if it exists)
	current_dir = os.getcwd()
	pidfile_path = os.path.join(tempfile.gettempdir(), '%s.pid' % __name__)

	# Read pid from pidfile
	pidfile = open(pidfile_path, "r")
	content = pidfile.readlines()
	pidfile.close()
	content = [x.strip() for x in content] # remove whitespace characters like `\n` at the end of each line
	# print content
	pid = int(content[0])

	# Kill process
	util.kill_proc_tree(pid)

	# Delete pidfile
	os.remove(pidfile_path)

	sys.stdout.write(' OK.\n')

class S(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	# /status
	# /announce
	# /configure
	# /echo
	# /list
	def do_GET(self):
		parsed_path = urlparse.urlparse(self.path)

		query_dict = urlparse.parse_qsl(urlparse.urlsplit(self.path).query)
		#print query_dict

		resource = parsed_path.path
		query = parsed_path.query
		#print "resource: %s" % resource
		#print "query: %s" % query

		if resource == '/status':

			# Set headers
			self.send_response(200)
			self.send_header('Content-Type', 'application/json')
			self.end_headers()

			# Generate data structure
			#builder_dir = os.path.abspath('/builder')
			builder_dir = os.getcwd()
			builderfile_path = os.path.abspath(os.path.join(builder_dir, 'Builderfile'))

			file = open(builderfile_path, 'r')
			filelines = file.readlines()
			file.close()

			device_uuid = 'N/A'
			device_name = 'N/A'
			device_ip = 'N/A'

			for i in range(len(filelines)):

				# Read human-readable name 
				if filelines[i].startswith('name:'):
					device_name = filelines[i].split(': ')[1]
					device_name = device_name.replace('\n', '')

				# Read UUID
				if filelines[i].startswith('uuid:'):
					device_uuid = filelines[i].split(': ')[1]
					device_uuid = device_uuid.replace('\n', '')

			status = {
				'name': device_name,
				'uuid': device_uuid
			}

			# Generate JSON for data structure
			status_json = json.dumps(status)

			# Write response
			self.wfile.write(status_json)

		elif resource == '/info':
			self._set_headers()
			self.wfile.write("<html><body><h1>info</h1></body></html>")

	def do_HEAD(self):
		self._set_headers()
																
	def do_POST(self):
		parsed_path = urlparse.urlparse(self.path)

		#query_dict = urlparse.parse_qsl(urlparse.urlsplit(self.path).query)
		#print query_dict

		resource = parsed_path.path
		query = parsed_path.query
		#print "resource: %s" % resource
		#print "query: %s" % query

		if resource == '/state':

			# Set headers
			self.send_response(200)
			self.send_header('Content-Type', 'application/json')
			#self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
			self.end_headers()

			# Parse request
			# Read request body and convert to dictionary.
			request = {}
			request['body'] = self.rfile.read(int(self.headers['Content-Length']))
			request_dict = json.loads(request['body'])

			# Process request
			#builder_dir = os.path.abspath('/builder')
			builder_dir = os.getcwd()
			builderfile_path = os.path.abspath(os.path.join(builder_dir, 'db_state.json'))

			# Load the record from database
			db_dict = {}
			file = open(builderfile_path, 'r+')
			db_dict = json.loads(file.read())
			file.close()

			# Update the record 
			for key in request_dict.keys():
				db_dict[key] = request_dict[key]
			db_dict_json = json.dumps(db_dict)

			# Write updated database
			file = open(builderfile_path, 'w+')
			file.write(db_dict_json)
			file.close()

			# Generate response (with JSON)
			response = {}
			#file = open(builderfile_path, 'r+')
			#response['body'] = file.read()
			#file.close()
			response['body'] = db_dict_json

			#response_json = json.dumps(request_dict)

			# Generate response (with JSON)
			#status = {
			#	'name': 'foo',
			#	'uuid': 'bar' 
			#}

			# Write response
			self.wfile.write('%s' % response['body'])

def run(server_class=HTTPServer, handler_class=S, port=80):
	sys.stdout.write('Starting httpd...\n')

	# Write pid into pidfile
	current_dir = os.getcwd()
	pidfile_path = os.path.join(tempfile.gettempdir(), '%s.pid' % __name__) # create the pidfile
	# TODO: get name of file for naming "builder.<filename>.pid"
	# TODO: tempfile.NamedTemporaryFile(prefix='builder.broadcast.', suffix='.pid').name
	pidfile = open(pidfile_path, "w+")
	#portalocker.lock(pidfile, portalocker.LOCK_EX) # lock the pidfile
	pidfile.write('%s' % os.getpid())
	pidfile.close()

	# Start HTTP server
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print 'Starting httpd...'
	httpd.serve_forever()

def run2(port=4445):

	# Write pid into pidfile
	current_dir = os.getcwd()
	pidfile_path = os.path.join(tempfile.gettempdir(), '%s.pid' % __name__) # create the pidfile
	# TODO: get name of file for naming "builder.<filename>.pid"
	# TODO: tempfile.NamedTemporaryFile(prefix='builder.broadcast.', suffix='.pid').name
	pidfile = open(pidfile_path, "w+")
	#portalocker.lock(pidfile, portalocker.LOCK_EX) # lock the pidfile
	pidfile.write('%s' % os.getpid())
	pidfile.close()

	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	serverSocket.bind(('', port))

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
				logger.info('Received: %s from %s' % (message, address))

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

			elif message.startswith('list'):
				response_message = list2() # remove "echo " from start of string
				print response_message
				serverSocket.sendto(response_message, address)

		except:
			None

	serverSocket.close()

def list2():
	builder_dir = os.path.abspath('/builder') # this will return current directory in which python file resides.
	builderfile_path = os.path.abspath(os.path.join(builder_dir, 'Builderfile')) # this will return current directory in which python file resides.
	# Read the Builderfile
	# TODO: Initialize the daemon here?
	file = open(builderfile_path, 'r')
	filelines = file.readlines()
	file.close()
	
	device_uuid = 'N/A'
	device_name = 'N/A'
	device_ip = 'N/A'

	for i in range(len(filelines)):

		# Read human-readable name 
		if filelines[i].startswith('name:'):
			device_name = filelines[i].split(': ')[1]
			device_name = device_name.replace('\n', '')

		# Read UUID
		if filelines[i].startswith('uuid:'):
			device_uuid = filelines[i].split(': ')[1]
			device_uuid = device_uuid.replace('\n', '')
	
	# Set IP address
	#device_ip = socket.gethostbyname(socket.gethostname())

	# Print the device listing
	#return "%s\t%s\t%s" % (device_name, device_uuid, device_ip)
	list_dict = {
		'name': device_name,
		'uuid': device_uuid
	}

	return json.dumps(list_dict)

if __name__ == "__main__":
	run()
