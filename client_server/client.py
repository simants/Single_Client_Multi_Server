#Shubham Simant
#1001860599
#srs0599@mavs.uta.edu

import pickle
import socket
import time

#Class for ServerA
class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # server A IPV4,TCP protocol
        self.client.connect((socket.gethostname(), 1904))
        self.header_size = 10

    def run_client(self):
        is_new_msg, full_msg, msg_len = (True, b'', None)
        while True:
            try:
                msg = self.client.recv(16)  # .recv is to accept the response
                if is_new_msg:
                    msg_len = int(msg[:self.header_size])
                    is_new_msg = False

                full_msg += msg

                if len(full_msg) - self.header_size == msg_len:
                    print("Message received from server")
                    my_msg = pickle.loads(full_msg[self.header_size:])
                    #   formatting the response
                    for name, value in my_msg.items():
                        size, data = value
                        print("{:35}{:15}{:10}".format(name, data, size))
                    # is_new_msg true will help to accept the msg again.
                    is_new_msg, full_msg, msg_len = (True, b'', None)
                    self.client.close()
                    break
            except ValueError:
                continue


#Initiating Client Class
if __name__ == '__main__':
    _client = Client()
    _client.run_client()
