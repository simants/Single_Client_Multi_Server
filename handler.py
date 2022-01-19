#Shubham Simant
#1001860599
#srs0599@mavs.uta.edu

import os
import sys

from dirsync import sync
from watchdog.events import FileSystemEventHandler

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

#Handler to check the changes in the dict_a and dict_b
class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        dirs = {
            'dict_a': 'dict_b',
            'dict_b': 'dict_a',
        }
        try:
            if event.is_directory:
                return None
        #Handling various events happening on dictonary

            elif event.event_type == 'created':
                for key, value in dirs.items():
                    if str(event.src_path).__contains__(key):
                        sync(key, value, 'sync')
            elif event.event_type == 'moved':
                for key, value in dirs.items():
                    if str(event.src_path).__contains__(key):
                        sync(key, value, 'sync', purge=True)
            elif event.event_type == 'deleted':
                for key, value in dirs.items():
                    if str(event.src_path).__contains__(key):
                        sync(key, value, 'sync', purge=True)
            elif event.event_type == 'modified':
                for key, value in dirs.items():
                    if str(event.src_path).__contains__(key):
                        sync(key, value, 'update')
            else:
                print('Invalid event: ' + str(event.event_type))
        except Exception:
            print('File synced is taking longer...')

