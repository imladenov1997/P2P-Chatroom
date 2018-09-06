import pickle
import threading


class Receiver(threading.Thread):
    def __init__(self, remote_socket, address, callbacks):
        threading.Thread.__init__(self)
        self.remote_socket = remote_socket
        self.update_address_list = callbacks['update_address_list']
        self.add_address = callbacks['add_address']
        self.send_address = callbacks['send_address']
        self.add_peer = callbacks['add_peer']
        self.remove_socket = callbacks['remove_socket']
        self.address = address
        self.port = -1

    def run(self):
        while True:
            try:
                msg = self.remote_socket.recv(4096).decode()
            except ConnectionResetError:
                print('Client left')
                self.remove_socket(self.address, self.port)
                return
            if msg == '*LST*':
                address_list = pickle.loads(self.remote_socket.recv(4096))
                self.update_address_list(address_list)
            elif msg.split(':')[0] == '*PRT*':
                self.port = int(msg.split(':')[1])
                result = self.add_address(self.address, self.port)
                if result:
                    self.send_address(self.address, self.port)
            elif msg.split(':')[0] == '*NEWADDR*':
                data = msg.split(':')
                host = data[1]
                port = data[2]
                self.add_peer(host, port)
            else:
                print(msg)