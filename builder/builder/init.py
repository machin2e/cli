# The Builderfile is used to bootstrap the Builder daemon which manages 
# the device's configuration and allows it to be edited in real-time 
# from smartphone and when plugged in over USB as mass storage.

# Create "Builderfile" that contains:
# - UUID
# - human-readable name

import os.path
import uuid
import petname

def init(name=None, virtual=False):
	builderfile_path = './Builderfile'

	# Create default Builderfile if it doesn't exist.
	if not os.path.exists(builderfile_path):
		file = open(builderfile_path, 'w')

		# Write human-readable name
		if name == None:
			name = petname.Generate(2)
		file.write("Name: %s\n" % name)

		# Write UUID
		device_uuid = uuid.uuid4()
		file.write("UUID: %s\n" % device_uuid)

		# Provider: builder, vagrant

		file.close()


	else:
		# Read the Builderfile
		# TODO: Initialize the daemon here?
		file = open(builderfile_path, 'r')
		filelines = file.readlines()

		for i in range(len(filelines)):

			# Read human-readable name 
			if filelines[i].startswith('Name:'):
				name = filelines[i].split(': ')[1]
				#print filelines[i]
				print name.replace('\n', '')

			# Read UUID
			if filelines[i].startswith('UUID:'):
				device_uuid = filelines[i].split(': ')[1]
				#print filelines[i]
				print device_uuid.replace('\n', '')

		file.close()

if __name__ == "__main__":
	#print "builder_init.py called directly"
	init()
#else:
	#print "builder_init.py module"
