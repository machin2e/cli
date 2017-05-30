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

	print util.get_builder_root()

	# Define command-line argument parser
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument("command")
	parser.add_argument("option1", nargs='?', default=None)
	parser.add_argument("option2", nargs='?', default=None)
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

	if not args.command == 'init':
		if not util.is_builder_tree():
			print 'Error: I can\'t do that.'
			print 'Reason: There is no .builder directory in the current or parent directories.'
			print 'Hint: Run `builder init`.' 
			return


	if args.command == "init":
		# Examples:
		# builder init						Used to initialize this folder (assigns a default name).
		# builder init -v					Used to create and init a VM (via Vagrant).
		# builder init fiery-fox -v			Used to initialize a new VM named fiery-fox.
		# builder init desktop				Used to init a Builder env called desktop.
		init(name=args.option1, virtual=args.virtual)
	elif args.command == "start":
		service.manage.start()
		service.announce.start()
	elif args.command == 'manage':
		if args.option1 == 'start':
			service.manage.start()
		elif args.option1 == 'run':
			service.manage.run()
		elif args.option1 == 'stop':
			service.manage.stop()
	elif args.command == 'announce':
		if args.option1 == 'start':
			service.announce.start()
		elif args.option1 == 'run':
			service.announce.run()
		elif args.option1 == 'stop':
			service.announce.stop()
	elif args.command == 'monitor':
		if args.option1 == 'start':
			None
		elif args.option1 == 'run':
			service.watchdir.run()
		elif args.option1 == 'stop':
			None
	

	elif args.command == 'project': # app
		if args.option1 == 'list':
			None
		elif args.option1 == 'add':
			None
		elif args.option1 == 'remove':
			None
	elif args.command == 'device':
		if args.option1 == 'list':
			list()
		elif args.option1 == 'add':
			device.add(args.option2)
		elif args.option1 == 'remove':
			None
	elif args.command == 'interface':
		if args.option1 == 'list':
			None
		elif args.option1 == 'add':
			None
		elif args.option1 == 'remove':
			None
	elif args.command == 'controller': # logic
		if args.option1 == 'add':
			None
		elif args.option1 == 'remove':
			None
	elif args.command == 'view':
		None
	elif args.command == 'design': # CAD design file
		None


	elif args.command == 'sync':
		sync(args.option1)
	elif args.command == 'ssh':
		ssh(args.option1)
	elif args.command == "echo":
		echo(args.option1)


	elif args.command == 'login':
		None
	elif args.command == 'logout':
		None
	elif args.command == 'signup':
		None
	elif args.command == 'whoami':
		None
	elif args.command == "clean":
		clean()

# TODO: INCORPORATE UDP I/O (LIKE ECHO) INTO LIST TO RETURN STRINGS FROM DEVICES. MAKE "listing" A PARAMETER IN DEVICE Builderfile. / "sync" (if not list): CREATES FOLDERS ON LOCAL SYSTEM FOR DISCOVERED DEVICES (ADD-ONLY UNLESS COMMAND TO CLEANUP/REBASE) WITH SYNC FOLDERS.
# TODO: COMMAND-LINE IASM. START WITH COMMAND ON A HOST/DEVICE: ./builder interface add mokogobo/ir-rangefinder ; THEN IT DOWNLOADS THE CONFIG FOR THE FILE, ASKS WHICH PINS TO USE (OR AUTO-SELECT, BASED ON INTERNAL STATE), THEN GIVES YOU ON-SCREEN INSTRUCTIONS TO ASSEMBLE/EDIT STATE.
# "IT'S ACTUALLY FUN TO PROGRAM BY JUMPING AROUND SEEING THE HIGHLIGHTED DEVICE SO YOU KNOW WHERE YOU'RE WORKING, AND SEEING HUD ON PHONE AND IN WINDOWS ON DESKTOP (SUMMONABLE/ASSIGNABLE VIA COMMAND LINE. SHOW UP AS SNAPPABLE WINDOWS. CAN SAVE AND CHANGE VIEWS WITH A COMMAND AS WELL. CAN MAKE ALWAYS ON TOP, TOO.).

if __name__ == "__main__":
	builder()
