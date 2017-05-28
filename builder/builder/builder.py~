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

def builder(command=None):

	# Define command-line argument parser
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument("command")
	parser.add_argument("option1", nargs='?', default=None)
	parser.add_argument("-v", "--virtual", action="store_true", help="specify virtual machine (use with init)")

	# Parse arguments
	args = None
	if not command == None:
		myargs = command.split(' ')
		args = parser.parse_args(myargs)
	else:
		args = parser.parse_args()

	# TODO: Search for all available "builder_*" files in toolchain and print error with command to repair the toolchain.
	
	"""
	CLI interface:
	
	signup
	login
	help
	note [add|remove|list]		Used to add, remove, or list notes for a device or environment/workspace/project.
	assemble			Starts interactive self-assembly.
	start [broadcast|discover]
	status [broadcast|discover]
	run [broadcast|discover]
	stop [broadcast|discover]
	monitor [broadcast|discover]

	log
	"""

	if args.command == 'login':
		None
	elif args.command == 'logout':
		None
	elif args.command == 'signup':
		None
	elif args.command == 'whoami':
		None
	elif args.command == "init":
		# Examples:
		# builder init						Used to initialize this folder (assigns a default name).
		# builder init -v					Used to create and init a VM (via Vagrant).
		# builder init fiery-fox -v			Used to initialize a new VM named fiery-fox.
		# builder init desktop				Used to init a Builder env called desktop.
		init(name=args.option1, virtual=args.virtual)
	elif args.command == "clean":
		clean()
	elif args.command == "start":
		if args.option1 == "announce":
			service.broadcast.start()
		elif args.option1 == "manager":
			service.manager.start()
		elif args.option1 == None:
			service.manager.start()
			service.broadcast.start()
        # TODO: 'monitor' like "less" command but for UDP traffic, HTTP traffic, etc. (without logging, to stdout)
	elif args.command == "run":
		if args.option1 == "announce":
			service.broadcast.run()
		elif args.option1 == 'manager':
			service.manager.run()
		elif args.option1 == 'monitor':
			service.watchdir.run()
	elif args.command == "stop":
		if args.option1 == 'announce':
			service.broadcast.stop()
		elif args.option1 == 'manager':
			service.manager.stop()
		if args.option1 == None:
			service.broadcast.stop()
			service.manager.stop()
	elif args.command == "up":
		# TODO: turn on machine if it's not already up!
		#ssh(args.option1)
		None
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
        elif args.command == 'rename':
            # TODO: Rename device!
            None
	elif args.command == "configure":
		# Examples:
		# builder configure name:Michael
		pair = args.option1.split(':')
		configure(pair[0], pair[1])
	elif args.command == 'add':
		if args.option1 == 'app':
			None
		elif args.option1 == 'interface':
			None # TODO: creates an interface directory with boilerplate configuration (if not specified in command), with file/folder structure
		elif args.option1 == 'controller':
			None
		elif args.option1 == 'view':
			None
		elif args.option1 == 'shape':
			None
	elif args.command == 'jump': # goto : changes into the interfaces or specific interface folder (if specified)
		if args.option1 == 'interface':
			None
	elif args.command == 'ls':
		if args.option1 == 'app':
			None
		elif args.option1 == 'interface':
			None
		elif args.option1 == 'controller':
			None
		elif args.option1 == 'view':
			None
		elif args.option1 == 'shape':
			None
	elif args.command == 'rm':
		if args.option1 == 'interface':
			None

# TODO: INCORPORATE UDP I/O (LIKE ECHO) INTO LIST TO RETURN STRINGS FROM DEVICES. MAKE "listing" A PARAMETER IN DEVICE Builderfile. / "sync" (if not list): CREATES FOLDERS ON LOCAL SYSTEM FOR DISCOVERED DEVICES (ADD-ONLY UNLESS COMMAND TO CLEANUP/REBASE) WITH SYNC FOLDERS.
# TODO: COMMAND-LINE IASM. START WITH COMMAND ON A HOST/DEVICE: ./builder interface add mokogobo/ir-rangefinder ; THEN IT DOWNLOADS THE CONFIG FOR THE FILE, ASKS WHICH PINS TO USE (OR AUTO-SELECT, BASED ON INTERNAL STATE), THEN GIVES YOU ON-SCREEN INSTRUCTIONS TO ASSEMBLE/EDIT STATE.
# "IT'S ACTUALLY FUN TO PROGRAM BY JUMPING AROUND SEEING THE HIGHLIGHTED DEVICE SO YOU KNOW WHERE YOU'RE WORKING, AND SEEING HUD ON PHONE AND IN WINDOWS ON DESKTOP (SUMMONABLE/ASSIGNABLE VIA COMMAND LINE. SHOW UP AS SNAPPABLE WINDOWS. CAN SAVE AND CHANGE VIEWS WITH A COMMAND AS WELL. CAN MAKE ALWAYS ON TOP, TOO.).

if __name__ == "__main__":
	builder()
