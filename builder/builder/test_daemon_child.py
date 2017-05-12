import subprocess
import sys

#p = subprocess.Popen(["python", "daemon.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
p = subprocess.Popen(["python", "daemon.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

for c in iter(lambda: p.stdout.read(1), ''):
	sys.stdout.write(c)
