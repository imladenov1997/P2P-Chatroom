import pickle
from pathlib import Path
from PairGenerator import PairGenerator
import socket

from Receiver import Receiver
from Sender import Sender


class Peer:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.addresses = {}
        self.address_list = []

    def check_keys(self, room_name):
        directory = 'keys/'
        public_key_path = directory + room_name + '_public.pem'
        private_key_path = directory + room_name + '_private.pem'

        public_key_file = Path(public_key_path)
        private_key_file = Path(private_key_path)

        if not (public_key_file.is_file() or private_key_file.is_file()):
            pair_generator = PairGenerator(public_key_path, private_key_path)
            pair_generator.generate_public_key()
            pair_generator.generate_private_key()

        self.public_key_file = Path(public_key_path)

    # Prepare connection initialisation where public key is read and prepared for sending
    def connect(self, remote_address, remote_port):
        if self.public_key_file.is_file():
            with self.public_key_file.open() as file:
                data = file.read()
                self.add_peer(remote_address, remote_port)

    # Request a connection to a peer
    def add_peer(self, remote_address, port):
        if not (remote_address == '' and port == ''):
            s = socket.socket()
            s.connect((remote_address, int(port)))
            s.send('*PRT*:'.encode())
            s.send(str(self.port).encode())
            callbacks = {
                'update_address_list': self.update_address_list,
                'add_address': self.add_address,
                'send_address': self.send_address,
                'add_peer': self.add_peer
            }
            full_address = remote_address + str(port)
            self.addresses[full_address] = {
                'receiver': Receiver(s, remote_address, callbacks),
                'socket': s,
                'port': None
            }
            self.addresses[full_address]['receiver'].start()

    # Initialise a connection to the socket
    def initialise_connection(self):
        self.local_socket = socket.socket()
        self.local_socket.bind((self.address, self.port))
        self.local_socket.listen(5)
        if self.address == 'localhost':
            self.address = '127.0.0.1'
        self.address_list.append(self.address + ':' + str(self.port))

        self.sender = Sender(self.local_socket, self.addresses)

        self.sender.start()

    # Listen for connections and once there is such, add this socket to the list
    def listen(self):
        while True:
            c, addr = self.local_socket.accept()
            print("User connected")
            callbacks = {
                'update_address_list': self.update_address_list,
                'add_address': self.add_address,
                'send_address': self.send_address,
                'add_peer': self.add_peer
            }
            self.addresses[addr] = {
                'receiver': Receiver(c, addr, callbacks),
                'socket': c,
                'port': None
            }
            self.addresses[addr]['receiver'].start()

            c.send('*LST*'.encode())
            c.send(pickle.dumps(self.address_list))

            print(self.addresses)
            print(self.address_list)

    def update_address_list(self, address_list):
        self.address_list = address_list
        print('LATEST ADDRESSES')
        print(self.address_list)
        print('LATEST ADDRESSES')

    def add_address(self, host, port):
        new_address = str(host[0]) + ':' + str(port)
        if new_address in self.address_list:
            return False

        self.addresses[host]['port'] = port
        self.address_list.append(new_address)
        return True

    def send_address(self, host, port):
        new_address = str(host[0]) + ':' + str(port)
        for address in self.addresses:
            print('NEW ADDRESS IS BEING SENT...')
            print(new_address)
            print('NEW ADDRESS IS SENT')
            if address[0] == host[0] and self.addresses[address]['port'] == port:
                continue
            self.addresses[address]['socket'].send(('*NEWADDR*:' + new_address).encode())

addr = input('Please enter an address:\n')
port = int(input('Enter port:\n'))

rm_addr = input('Please enter an address or skip for a new chatroom:\n')
rm_port = input('Remote port:\n')

peer = Peer(addr, port)
peer.check_keys('FirstRoom')
peer.initialise_connection()

peer.connect(rm_addr, rm_port)
peer.listen()




