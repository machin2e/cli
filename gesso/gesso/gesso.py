#!/usr/bin/env python
from imports import *
import argparse
import api
import util

import os # used for git

def gesso(command=None):

	# TODO: Make parsers arguments optional arguments only show up for relevant argument trees.
	# TODO: make sure `gesso new` was called prior to other commands!
	# TODO: during `gesso new`, load device .yaml files into memory! then can set state and push to device (and sync, eventually)
	# TODO: don't worry about filesystem too much for now... just load model (proxy for download), then update state through API... DO THIS IN CONTROLLER? NOT CLI? PROBALBY!!!!!!!

	# Define command-line argument parser
	parser = argparse.ArgumentParser(description='Gesso command-line interpreter.')
	parser.add_argument('command')
	parser.add_argument('option1', nargs='?', default=None)
	parser.add_argument('option2', nargs='?', default=None)
	parser.add_argument('-v', '--virtual', action='store_true', help='specify virtual machine (use with new)')
	parser.add_argument('-r', '--role', default='workspace', choices=['workspace','gesso'], help='specify role of gesso context (use with new)')
	parser.add_argument('--component', action='append', dest='models', nargs='?', default=[], help='Add models for command.')

	# Parse arguments
	args = None
	if not command == None:
		myargs = command.split(' ')
		args = parser.parse_args(myargs)
	else:
		args = parser.parse_args()

	# TODO: Search for all available "gesso_*" files in toolchain and print error with command to repair the toolchain.

	if not args.command == 'new':
		if not util.is_gesso_tree():
			print 'Error: I can\'t do that.'
			print 'Reason: There is no .gesso directory in the current or parent directories.'
			print 'Hint: Run `gesso new`.' 
			return

	if args.command == 'port':
		#path = os.path.join(util.get_gesso_root(), '_robot', 'motors', 'right-servo', 'model-device-gesso.yaml')
		path = os.path.join(util.get_gesso_root(), '.gesso', 'components', 'gesso-8.0.0.yaml')
		d = api.Device(path=path)
		for port in d.get_ports():
			print port.mode
			print port.direction
			print port.voltage
		print port.states
	
		return

	if args.command == "new":
		new(name=args.option1, role=args.role)

	elif args.command == "status":
		# TODO: Print current status. Ex: 'running', 'paused', 'stopped'
		None	

	elif args.command == "start":
		# TODO: for hosts, load their own device file, and the device files for connected peripherals, their controllers, etc.; new in-memory state of board
		service.manage.start()
		service.announce.start()
	elif args.command == "pause":
		service.manage.stop()
		service.announce.stop()
		# TODO: Suspend VMs! `vagrant suspend` (Y/N)
	elif args.command == "resume":
		service.manage.start()
		service.announce.start()
		# TODO: Resume VMs! `vagrant resume` (if suspended)
	elif args.command == "stop":
		service.manage.stop()
		service.announce.stop()
		# TODO: Start VMs! `vagrant suspend`
	elif args.command == 'announce':
		if args.option1 == 'start':
			service.announce.start()
		elif args.option1 == 'run':
			service.announce.run()
		elif args.option1 == 'stop':
			service.announce.stop()
	elif args.command == 'manage':
		if args.option1 == 'start':
			service.manage.start()
		elif args.option1 == 'run':
			service.manage.run()
		elif args.option1 == 'stop':
			service.manage.stop()
	elif args.command == 'monitor':
		if args.option1 == 'start':
			None
		elif args.option1 == 'run':
			service.watchdir.run()
		elif args.option1 == 'stop':
			None
	

	elif args.command == 'assemble':
		assemble(args.models)

	elif args.command == 'project': # app
		if args.option1 == 'list':
			None
		elif args.option1 == 'add':
			None
		elif args.option1 == 'remove':
			None

	elif args.command == 'component':
		if args.option1 == 'list':
			device.list(args.option2)
		elif args.option1 == 'search':
			# TODO: Search device registry for a device name/description matching specified string/regex
			None
		elif args.option1 == 'add':
			device.add(args.option2, virtual=args.virtual)
		elif args.option1 == 'start':
			device.start(args.option2)
		elif args.option1 == 'ssh':
			device.ssh(args.option2)
		elif args.option1 == 'restart':
			device.restart(args.option2)
		elif args.option1 == 'pause':
			device.pause(args.option2)
		elif args.option1 == 'stop':
			device.stop(args.option2)
		elif args.option1 == 'remove':
			device.remove(args.option2)

	elif args.command == 'interface':
		if args.option1 == 'list':
			None
		elif args.option1 == 'add':
			interface.add(args.option2)
		elif args.option1 == 'remove':
			interface.remove(args.option2)
		elif args.option1 == 'compose':
			# TODO: Composes multiple interfaces under a new interface. Generates interface file with dependencies.
			None
	elif args.command == 'controller': # logic
		if args.option1 == 'list':
			None
		elif args.option1 == 'add':
			None
		elif args.option1 == 'remove':
			None
	elif args.command == 'view':
		if args.option1 == 'list':
			None
		elif args.option1 == 'add':
			None
		elif args.option1 == 'remove':
			None
	elif args.command == 'material': # Alt: 'design', 'asset' (CAD design file)
		None

	# gesso port add digital,output,ttl --interface servo
	# gesso port add digital,output,ttl --interface servo
	# gesso port add digital,output,ttl --interface servo

	# gesso interface deploy|assign <device-name>

	# gesso interface assemble|install

	# gesso assemble|install

	# gesso deploy

	elif args.command == 'log':
		# TODO: gesso [device <name>] log <announce|manage|command>
		None

	elif args.command == 'sync':
		sync(args.option1)

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

	elif args.command == "version":
		api.version()
	
	else:
		print 'Error: I can\'t do that.'
		print 'Reason: Unrecognized expression.'
		print 'Hint: Run `gesso help` to see what I can do.'

if __name__ == "__main__":
	gesso()
