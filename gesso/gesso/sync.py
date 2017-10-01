import os, sys
import pexpect, subprocess
import time
import socket, json
import util

def sync(name, username='vagrant'):

	# Initialize logging
	unison_log = util.logger('unison')

	#process = subprocess.Popen(['vagrant', 'ssh', name], stdout=subprocess.PIPE, cwd=os.path.dirname(os.path.realpath(__file__)), bufsize=1)
	cwd = os.path.dirname(os.path.realpath(__file__))
	device_name = name #device_name = 'great-spider' # TODO: Send message to great-spider to get its IP.

	# TODO: Cache this! Get cached IP address from LUT.
	device_ip = util.request_ip_address(name)
        unison_log = util.logger('unison')

	if device_ip != None:
		current_dir = os.getcwd()
		process = subprocess.Popen(['unison',
									'-sshargs', "'-o StrictHostKeyChecking=no'",
									'-auto', '-batch',
									device_name, 'ssh://vagrant@%s//builder' % device_ip], 
								   stdout=subprocess.PIPE,
								   stdin=subprocess.PIPE,
								   stderr=subprocess.PIPE,
								   shell=False,
								   cwd=current_dir,
								   bufsize=1)

		sys.stdout.write("Syncing. ")

		# Log stdout and stderr for Unison synchronization process.
		# This can be used for debugging.
		stdout, stderr = process.communicate()
		if stdout:
			unison_log.info(stdout)
		if stderr:
			unison_log.error(stderr)

		sys.stdout.write("Done. ")

		#while True:
		#	#output = process.stdout.readline()
		#	output = process.stdout.read(1)
		#	if output == '' and process.poll() is not None:
		#		break
		#	if output:
		#		#sys.stdout.write(output)
		#		#sys.stdout.flush()
		#		##print output.strip(),
		#		None

if __name__ == "__main__":
	sync()
