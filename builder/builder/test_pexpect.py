import pexpect
from pexpect.popen_spawn import PopenSpawn
import sys

import os

# References:
# - https://stackoverflow.com/questions/2408560/python-nonblocking-console-input
# - https://code.activestate.com/recipes/197140-key-press-detection-for-windows-text-only-console-/
# - https://stackoverflow.com/questions/11457931/running-an-interactive-command-from-within-python

# Windows
if os.name == 'nt':
    import msvcrt

# Posix (Linux, OS X)
else:
    import sys
    import termios
    import atexit
    from select import select

#child = pexpect.spawn('bash')
#child.interact()

class KBHit:

    def __init__(self):
        '''Creates a KBHit object that you can call to do various keyboard things.
        '''
        if os.name == 'nt':
            pass

        else:

            # Save the terminal settings
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)

            # New terminal setting unbuffered
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

            # Support normal-terminal reset at exit
            atexit.register(self.set_normal_term)


    def set_normal_term(self):
        ''' Resets to normal terminal.  On Windows this is a no-op.
        '''

        if os.name == 'nt':
            pass

        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


    def getch(self):
        ''' Returns a keyboard character after kbhit() has been called.
            Should not be called in the same program as getarrow().
        '''

        s = ''

        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')

        else:
            return sys.stdin.read(1)


    def getarrow(self):
        ''' Returns an arrow-key code after kbhit() has been called. Codes are
        0 : up
        1 : right
        2 : down
        3 : left
        Should not be called in the same program as getch().
        '''

        if os.name == 'nt':
            msvcrt.getch() # skip 0xE0
            c = msvcrt.getch()
            vals = [72, 77, 80, 75]

        else:
            c = sys.stdin.read(3)[2]
            vals = [65, 67, 66, 68]

        return vals.index(ord(c.decode('utf-8')))


    def kbhit(self):
        ''' Returns True if keyboard character was hit, False otherwise.
        '''
        if os.name == 'nt':
            return msvcrt.kbhit()

        else:
            dr,dw,de = select([sys.stdin], [], [], 0)
            return dr != []


kb = KBHit()

#child = pexpect.popen_spawn.PopenSpawn('cmd.exe')
cwd = os.path.dirname(os.path.realpath(__file__))
cwd = os.path.join(os.path.dirname(os.path.realpath(__file__)), '.builder', 'vagrant')
print cwd
child = pexpect.popen_spawn.PopenSpawn('vagrant ssh fiery-fox', cwd=cwd)
#child = pexpect.popen_spawn.PopenSpawn('bash -c "vagrant ssh fiery-fox"', cwd=cwd)
#child.expect('>')
#print child.before
buffer = ""
while True:
	#child.expect('%')
	# Read output from process

	# Read input and forward to process
	#input = raw_input()
	if kb.kbhit():
		c = kb.getch()
		if ord(c) == 13: #13: # 27: # ESC
			#print len(buffer)
			#child.sendline(buffer)
			child.send(buffer + "\n")
			#child.send(buffer + "\r\n")
			buffer = ""
		else:
			buffer += str(c)

		# echo input locally
		sys.stdout.write(c)
		sys.stdout.flush()

	output = child.read_nonblocking(size=1, timeout=0.1)
	if (len(output) > 0):
		sys.stdout.write(output)
		sys.stdout.flush()
		#output = child.read_nonblocking(size=1, timeout=0.1)
