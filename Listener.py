import socket
import threading


class Listener(threading.Thread):
    def __init__(self, local_socket):
        threading.Thread.__init__(self)
        self.local_socket = local_socket


    def run(self):
        self.local_socket.listen(5)

        while True:
            c, addr = self.local_socket.accept()
            print("User connected")
            threadSender = socketThread(c, threadID)
            threadListener = listeningThread(c, threadID)
            sockets[threadID] = c
            threadSender.start()
            threadListener.start()

