# The Builderfile is used to bootstrap the Builder daemon which manages 
# the device's configuration and allows it to be edited in real-time 
# from smartphone and when plugged in over USB as mass storage.

# Create "Builderfile" that contains:
# - UUID

import os.path
import uuid

builderfile_path = './Builderfile'

# Create default Builderfile if it doesn't exist.
if not os.path.exists(builderfile_path):
	uuid = uuid.uuid4()
	file = open(builderfile_path, 'w')
	file.write("UUID: %s" % uuid)
	file.close()


# Read the Builderfile
# TODO: Initialize the daemon here?
file = open(builderfile_path, 'r')
filelines = file.readlines()

for i in range(len(filelines)):

	# Read UUID
	if filelines[i].startswith('UUID:'):
		uuid = filelines[i].split(': ')[1]
		#print filelines[i]
		print uuid


