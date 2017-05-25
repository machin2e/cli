import os, sys
import time
import logging
from ..sync import sync
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

class SynchronizationEventHandler(FileSystemEventHandler):

	def on_moved(self, event):
		super(SynchronizationEventHandler, self).on_moved(event)

		#sys.stdout.write("modified => syncing!\n")
		#sys.stdout.flush()
		sync('saving-goat')

	def on_created(self, event):
		super(SynchronizationEventHandler, self).on_created(event)

		#sys.stdout.write("modified => syncing!\n")
		#sys.stdout.flush()
		sync('saving-goat')
	
	def on_deleted(self, event):
		super(SynchronizationEventHandler, self).on_deleted(event)

		#sys.stdout.write("modified => syncing!\n")
		#sys.stdout.flush()
		sync('saving-goat')
	
	def on_modified(self, event):
		super(SynchronizationEventHandler, self).on_modified(event)

		#sys.stdout.write("modified => syncing!\n")
		#sys.stdout.flush()
		sync('saving-goat')

def run():
	#path = sys.argv[1] if len(sys.argv) > 1 else '.'
	path = os.getcwd()
	sys.stdout.write('%s' % path)
	sys.stdout.flush()
	#event_handler = LoggingEventHandler()
	event_handler = SynchronizationEventHandler()
	observer = Observer()
	observer.schedule(event_handler, path, recursive=True)
	observer.start()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
		observer.join()

if __name__ == "__main__":
	run()
