#Shubham Simant
#1001860599
#srs0599@mavs.uta.edu

import os
import pickle
import socket
from datetime import datetime


from hurry.filesize import size, alternative


#Class for ServerA
class ServerB:
    def __init__(self):
        self.source_path = 'dict_b'
    #Creating connection with serverA
        self.server_b_server_a_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # .bind and .listen is used to bind socket to current host and port to listen
        self.server_b_server_a_sock.bind((socket.gethostname(), 2003))
        self.server_b_server_a_sock.listen(10)
        self.header_size = 10

    def run_server_b(self):
        while True:
            dir_b_dict = {}
            # Accepting the request made by Server-A to Server-B
            server_socket, address = self.server_b_server_a_sock.accept()
            print(f"Connection from {address} has been established.")
            # Listing the files in the dictionary B
            list_of_files = sorted(filter(lambda x: os.path.isfile(os.path.join(self.source_path, x)),
                                          os.listdir(self.source_path)))
            # for loop which is used to get size and date of files in dic_b
            for i in list_of_files:
                lists = [datetime.fromtimestamp(os.path.getmtime(self.source_path + '/' + i)).strftime('%d-%b'),
                         size(os.path.getsize(self.source_path + '/' + i), system=alternative)]
                dir_b_dict.update({i: lists})
            # it sends the response data in bytes
            msg = pickle.dumps(dir_b_dict)
            print(dir_b_dict)
            # the utf-8 is used for encoding the msg
            msg = bytes(f"{len(msg):<{self.header_size}}", 'utf-8') + msg
            # .send is used to send the msg for the request.
            server_socket.send(msg)

#Initiating ServerA Class
if __name__ == '__main__':
    server_b = ServerB()
    server_b.run_server_b()
