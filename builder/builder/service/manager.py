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

def start():
	# Initialize logging
	logger = util.logger(__name__)

	sys.stdout.write('Starting manager service.')

	current_dir = os.getcwdu()
	p = subprocess.Popen(['builder', 'run', 'manager'], cwd=current_dir)
	sys.stdout.write(' OK.\n')

	# Log status
	logger.info('Started manager service.')

def stop():
	sys.stdout.write('Stopping manager service.')

	# Log status
	logger = util.logger(__name__)
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

		# Status:
		# - role
		# - discovery status
		# - CoAP server status
		# - HTTP server status
		# - current project UUID
		# - current connected devices
	  if resource == '/status':

		# Set headers
		self.send_response(200)
		self.send_header('Content-Type', 'application/json')
		self.end_headers()

		# Generate response
		builderfile = util.load_builderfile()
		status_json = json.dumps(builderfile, indent=4, sort_keys=False)

		# Write response
		self.wfile.write(status_json)

	  elif resource == '/list':

		# Set headers
		self.send_response(200)
		self.send_header('Content-Type', 'application/json')
		self.end_headers()

		# Generate response
		listing = generate_listing()
		listing_json = json.dumps(listing, indent=4, sort_keys=False)

		# Generate JSON for data structure
		response_body = listing_json

		# Write response
		self.wfile.write(response_body)
		
	  elif resource == '/state':

		# Set headers
		self.send_response(200)
		self.send_header('Content-Type', 'application/json')
		self.end_headers()

		# Generate data structure
		#builder_dir = os.path.abspath('/builder')
		builder_dir = os.getcwdu()
		builderfile_path = os.path.abspath(os.path.join(builder_dir, 'db_state.json'))

		# Load the record from database
		db_dict = {}
		file = open(builderfile_path, 'r')
		db_dict = json.loads(file.read())
		file.close()
		db_dict_json = json.dumps(db_dict, indent=4, sort_keys=False)

		# Generate JSON for data structure
		response_body = db_dict_json

		# Write response
		self.wfile.write(response_body)

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

		# Preprocess request:
		# Cache volatile data
		#self.content_length = int(self.headers['Content-Length'])
		self.content_body = self.rfile.read(int(self.headers['Content-Length']))

		# Log request
		logger = util.logger(__name__)
		logger.info('\nPOST %s\n%s\n%s\n' % (self.path, self.headers, self.content_body))

		# Set headers
		self.send_response(200)
		self.send_header('Content-Type', 'application/json')
		#self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
		self.end_headers()

		# Parse request:
		# Read request body and convert to dictionary.
		request = {}
		#request['body'] = self.rfile.read(int(self.headers['Content-Length']))
		request['body'] = self.content_body
		#logger.info('\n\n%s\n\n' % request['body'])
		#logger.info('\n--BODY--\n%s\n^^BODY^^\n' % request['body'])
		#request_dict = json.loads(request['body'])
		#request_dict = json.loads(request_body)
		request_dict = json.loads(request['body'])
		logger.info('%s' % json.dumps(request_dict, indent=4, sort_keys=False))

		# Process request
		#builder_dir = os.path.abspath('/builder')
		builder_dir = os.getcwd()
		builderfile_path = os.path.abspath(os.path.join(builder_dir, 'db_state.json'))
		logger.info(builderfile_path)

		# Load the record from database
		db_dict = {}
		file = open(builderfile_path, 'r')
		db_dict = json.loads(file.read())
		file.close()
		#logger.info('%s' % json.dumps(db_dict, indent=4, sort_keys=False))

		# Update the record 
		for key in request_dict.keys():
			db_dict[key] = request_dict[key]
		db_dict_json = json.dumps(db_dict, indent=4, sort_keys=False)
		#logger.info('---\n%s\n---' % db_dict_json)

		# Write updated database
		file = open(builderfile_path, 'w')
		file.write(db_dict_json)
		file.close()

		# Generate response (with JSON)
		response = {}
		#file = open(builderfile_path, 'r')
		#response['body'] = file.read()
		#file.close()
		#response['body'] = db_dict_json

		response['body'] = db_dict_json

		# Generate response (with JSON)
		#status = {
		#	'name': 'foo',
		#	'uuid': 'bar' 
		#}

		# Write response
		self.wfile.write('%s' % response['body'])

def run(server_class=HTTPServer, handler_class=S, port=80):
	print 'Starting HTTP server.'

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

	print ' OK.'
	httpd.serve_forever()

# is_builder_dir(path)
# get_builder_dir()
# get_current_dir()
# get_builder_dir_type(path) # returns 'controller' or 'programmer'/'orchestrator'

# Returns true if the path contains a valid Builderfile.
# TODO: Check validity of Builderfile.
def is_builder_path(path=os.getcwd()):
	builderfile_path = os.path.join(path, 'Builderfile')
	if os.path.exists(builderfile_path):
		return True
	else:
		return False

# TODO: Consider renaming to is_programmer_path() or is_composer_path() or is_assembler_path()
# TODO: Make sure this doesn't return true when on a coordinator in a sync folder. Check parent directory for Builderfile of coordinator.
def is_controller_path(path=os.getcwd()):
	# Load the Builderfile
	builderfile = util.load_builderfile(path)
	
	# Check the 'role' field
	if 'role' in builderfile and builderfile['role'] == 'controller':
		return True

	return False

# TODO: Consider renaming to is_orchestrator_path() or is_planner_path()
def is_coordinator_path(path=os.getcwd()):
	# Load the Builderfile
	builderfile = util.load_builderfile(path)
	
	# Check the 'role' field
	if 'role' in builderfile and builderfile['role'] == 'coordinator':
		return True

	return False

def generate_listing():
	builderfile = util.load_builderfile()
	return builderfile 

if __name__ == "__main__":
	run()
