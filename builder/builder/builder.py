#!/usr/bin/env python

# The Builderfile is used to bootstrap the Builder daemon which manages
# the device's configuration and allows it to be edited in real-time
# from smartphone and when plugged in over USB as mass storage.

# Create "Builderfile" that contains:
# - UUID

# This file can also be loaded as module to access the Builder API from a Python script.

from imports import *
import os
import argparse
import petname
import util

data_dir = util.get_data_dir()
print data_dir

def builder(command=None):

	# Define command-line argument parser
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument("command")
	parser.add_argument("option1", nargs='?', default=None)
	parser.add_argument("-v", "--virtual", action="store_true", help="specify virtual machine (use with init)")
	#parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
	#parser.add_argument('--sum', dest='accumulate', action='store_const', const=sum, default=max, help='sum the integers (default: find the max)')

	# Parse arguments
	args = None
	if not command == None:
		myargs = command.split(' ')
		args = parser.parse_args(myargs)
	else:
		args = parser.parse_args()

	# TODO: Search for all available "builder_*" files in toolchain and print error with command to repair the toolchain.

	# TODO: signup
	# TODO: login
	# TODO: help
	# TODO: note [add|remove|list]		Used to add, remove, or list notes for a device or environment/workspace/project.
	# TODO: assemble			Starts interactive self-assembly.
	# TODO: start broadcast
	# TODO: start discover
	# TODO: status broadcast
	# TODO: status discover
	# TODO: stop broadcast
	# TODO: stop discover
	if args.command == "init":
		# Examples:
		# builder init						Used to initialize this folder (assigns a default name).
		# builder init -v					Used to create and init a VM (via Vagrant).
		# builder init fiery-fox -v			Used to initialize a new VM named fiery-fox.
		# builder init desktop				Used to init a Builder env called desktop.
		init(name=args.option1, virtual=args.virtual)
	elif args.command == "clean":
		clean()
	elif args.command == "start":
		if args.option1 == "broadcast":
			service.broadcast.start()
		elif args.option1 == "manager":
			service.manager.start()
		elif args.option1 == None:
			service.manager.start()
			service.broadcast.start()
	elif args.command == "run":
		if args.option1 == "broadcast":
			service.broadcast.run()
		elif args.option1 == 'manager':
			service.manager.run()
	elif args.command == "stop":
		if args.option1 == 'broadcast':
			service.broadcast.stop()
		elif args.option1 == 'manager':
			service.manager.stop()
		if args.option1 == None:
			service.broadcast.stop()
			service.manager.stop()
	elif args.command == "ssh":
		ssh(args.option1)
	elif args.command == "sync":
		sync(args.option1)
	elif args.command == "echo":
		echo(args.option1)
	elif args.command == "list":
		# Examples:
		# TODO: builder @fiery-fox start discovery
		# TODO: builder start discovery @fiery-fox
		list()
	elif args.command == "configure":
		# Examples:
		# builder configure name:Michael
		pair = args.option1.split(':')
		configure(pair[0], pair[1])

# TODO: INCORPORATE UDP I/O (LIKE ECHO) INTO LIST TO RETURN STRINGS FROM DEVICES. MAKE "listing" A PARAMETER IN DEVICE Builderfile. / "sync" (if not list): CREATES FOLDERS ON LOCAL SYSTEM FOR DISCOVERED DEVICES (ADD-ONLY UNLESS COMMAND TO CLEANUP/REBASE) WITH SYNC FOLDERS.
# TODO: COMMAND-LINE IASM. START WITH COMMAND ON A HOST/DEVICE: ./builder interface add mokogobo/ir-rangefinder ; THEN IT DOWNLOADS THE CONFIG FOR THE FILE, ASKS WHICH PINS TO USE (OR AUTO-SELECT, BASED ON INTERNAL STATE), THEN GIVES YOU ON-SCREEN INSTRUCTIONS TO ASSEMBLE/EDIT STATE.
# "IT'S ACTUALLY FUN TO PROGRAM BY JUMPING AROUND SEEING THE HIGHLIGHTED DEVICE SO YOU KNOW WHERE YOU'RE WORKING, AND SEEING HUD ON PHONE AND IN WINDOWS ON DESKTOP (SUMMONABLE/ASSIGNABLE VIA COMMAND LINE. SHOW UP AS SNAPPABLE WINDOWS. CAN SAVE AND CHANGE VIEWS WITH A COMMAND AS WELL. CAN MAKE ALWAYS ON TOP, TOO.).

if __name__ == "__main__":
	builder()

# Reference:
# - argparse: https://docs.python.org/3/library/argparse.html#module-argparse
# - argparse tutorial: https://docs.python.org/3/howto/argparse.html#id1
