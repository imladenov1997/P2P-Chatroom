import threading


class Sender(threading.Thread):
    def __init__(self, local_socket, addresses):
        threading.Thread.__init__(self)
        self.local_socket = local_socket
        self.addresses = addresses

    def run(self):
        while True:
            msg = input('Please enter your message:\n')
            print(self.addresses)
            for address in self.addresses:
                self.addresses[address]['socket'].send(msg.encode())
