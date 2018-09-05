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
        self.address = address

    def run(self):
        while True:
            msg = self.remote_socket.recv(4096).decode()
            if msg == '*LST*':
                address_list = pickle.loads(self.remote_socket.recv(4096))
                self.update_address_list(address_list)
            elif msg.split(':')[0] == '*PRT*':
                port = int(msg.split(':')[1])
                result = self.add_address(self.address, port)
                if result:
                    self.send_address(self.address, port)
            elif msg.split(':')[0] == '*NEWADDR*':
                data = msg.split(':')
                host = data[1]
                port = data[2]
                self.add_peer(host, port)
            else:
                print(msg)