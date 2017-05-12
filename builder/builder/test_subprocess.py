import subprocess
import os
import sys

#process = subprocess.Popen(['echo', '"Hello stdout"'], stdout=subprocess.PIPE)
#process = subprocess.Popen(['python', 'daemon.py'], stdout=subprocess.PIPE, bufsize=1)
process = subprocess.Popen(['python', 'daemon.py'], stdout=subprocess.PIPE, cwd=os.path.dirname(os.path.realpath(__file__)), bufsize=1)

#stdout = process.communicate()[0]
#print 'STDOUT:{}'.format(stdout)

#while process.poll() is None:
	#l = process.stdout.readline()
	#print l

while True:
	#output = process.stdout.readline()
	output = process.stdout.read(1)
	if output == '' and process.poll() is not None:
		break
	if output:
		#sys.stdout.write(out)
		#sys.stdout.flush()
		print output.strip(),
#rc = process.poll()
