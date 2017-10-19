#!/usr/bin/env python
from imports import *
import argparse
import api
import util
import os

def gesso(command=None):
    """
    Gesso's top-level command interpreter.
    """

    # Define command-line argument parser
    parser = argparse.ArgumentParser(description='Gesso command-line interpreter.')
    parser.add_argument('command')
    parser.add_argument('option1', nargs='?', default=None)
    parser.add_argument('option2', nargs='?', default=None)
    parser.add_argument('-v', '--virtual', action='store_true', help='specify virtual machine (use with new)')
    parser.add_argument('-r', '--role', default='workspace', choices=['workspace','gesso'], help='specify role of gesso context (use with new)')
    parser.add_argument('--component', action='append', dest='component_identifiers', nargs='?', default=[], help='Add component for command.')

    # Parse arguments
    args = None
    if not command == None:
        myargs = command.split(' ')
        args = parser.parse_args(myargs)
    else:
        args = parser.parse_args()

    # Preprocessors
    if not args.command == 'new':
        if not util.is_gesso_tree():
            print 'Error: I can\'t do that.'
            print 'Reason: There is no .gesso directory in the current or parent directories.'
            print 'Hint: Run `gesso new`.'
            return

    # Processors
    if args.command == "new":
        new(name=args.option1, role=args.role)
    elif args.command == "status":
        """
        TODO: Print current status. Ex: 'running', 'paused', 'stopped'
        """
        None
    elif args.command == "start":
        service.manage.start()
        service.announce.start()
    elif args.command == "stop":
        service.manage.stop()
        service.announce.stop()
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
    elif args.command == 'compose':
        assemble(args.component_identifiers)
    elif args.command == 'project':
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
            None
    elif args.command == 'controller':
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
    elif args.command == 'log':
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
