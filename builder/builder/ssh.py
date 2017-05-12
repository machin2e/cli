import subprocess
import os
import sys

import pexpect

def ssh(name):
	#cwd = os.path.dirname(os.path.realpath(__file__))
	#cwd = os.path.join(os.getcwd(), '.builder', 'vagrant')
	cwd = os.path.join(os.path.dirname(__file__), '.builder', 'vagrant')
	print cwd 
	p = pexpect.spawn('vagrant ssh %s' % name, cwd=cwd)
	p.setecho(False)

	def echoback(stringin):
		p.sendline(stringin)
		echoback = p.readline()
		return echoback.decode()

def ssh2(name):
	#process = subprocess.Popen(['vagrant', 'ssh', name], stdout=subprocess.PIPE, cwd=os.path.dirname(os.path.realpath(__file__)), bufsize=1)
	cwd = os.path.dirname(os.path.realpath(__file__))
	print cwd 
	process = subprocess.Popen(['vagrant', 'ssh', name], 
	                           stdout=subprocess.PIPE,
							   stdin=subprocess.PIPE,
							   shell=False,
							   cwd='.builder/vagrant', 
							   bufsize=1)

	while True:
		#output = process.stdout.readline()
		output = process.stdout.read(1)
		if output == '' and process.poll() is not None:
			break
		if output:
			sys.stdout.write(output)
			sys.stdout.flush()
			#print output.strip(),

if __name__ == "__main__":
	ssh()
