#Shubham Simant
#1001860599
#srs0599@mavs.uta.edu

import os
import pickle
import socket
import sys
import time
import traceback
from datetime import datetime

from dirsync import sync
from hurry.filesize import size, alternative
from watchdog.observers import Observer

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from handler import Handler

#Class for ServerA
class ServerA:
    def __init__(self):
        self.header_size = 10
        self.source_path = 'dict_a'
        self.target_path = 'dict_b'
        self.dirs = {
            self.source_path: self.target_path,
            self.target_path: self.source_path
        }
        self.client_server_a_sock = None
        self.server_b_server_a_sock = None
        self.observer = Observer()

    # Creating connection with server-client
    def start_connections(self):
        self.client_server_a_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # server A IPV4,TCP protocol
        self.client_server_a_sock.bind((socket.gethostname(), 1904))  # serverA-client bind
        self.client_server_a_sock.listen(5)  # used to listen to request
        self.client_server_a_sock.setblocking(False)

        self.server_b_server_a_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # server B IPV4,TCP protocol
        self.server_b_server_a_sock.connect((socket.gethostname(), 2003))  # serverA-serverB connection

    def run_server_a(self):
    #Implementing Oberserver for changes in directory A and B
        self.start_connections()
        try:
            self.sync_initial_files()
            for src, dist in self.dirs.items():
            #Handler to make the required changes to the either of dict_a or dict_b
                event_handler = Handler()
                self.observer.schedule(event_handler, src, recursive=True)
            self.observer.start()
            try:
                while True:
                    time.sleep(3)
                    self.send_message_client()
            except Exception:
                self.observer.stop()
                traceback.print_exc()
                print('Server A Exception')
            self.observer.join()
        except Exception:
            traceback.print_exc()
            self.client_server_a_sock.close()

    def send_message_client(self):
        if not self.client_server_a_sock:
            return
        dir_a_dict = {}
        list_of_files = sorted(filter(lambda x: os.path.isfile(os.path.join(self.source_path, x)),
                                      os.listdir(self.source_path)))
    #Sorting the list of files in dictonary
        for i in list_of_files:
            lists = [datetime.fromtimestamp(os.path.getctime(self.source_path + '/' + i)).strftime('%d-%b'),
                     size(os.path.getsize(self.source_path + '/' + i), system=alternative)]
            dir_a_dict.update({i: lists})
        sorted(dir_a_dict)
        print('Sending this sorted list to client')
        msg = pickle.dumps(dir_a_dict)
        msg = bytes(f"{len(msg):<{self.header_size}}", 'utf-8') + msg
        client_socket, address = (None, None)

    #Accpeting connection from client
        try:
            client_socket, address = self.client_server_a_sock.accept()
            if client_socket:
                client_socket.send(msg)
        except Exception:
            pass

#Sync items in Dir
    def sync_initial_files(self):
        for src, target in self.dirs.items():
            sync(src, target, 'update')
            sync(src, target, 'sync')

#Initiating ServerA Class
if __name__ == '__main__':
    server_a = ServerA()
    server_a.run_server_a()
