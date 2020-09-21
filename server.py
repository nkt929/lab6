import socket
import os
import math

from threading import Thread, Lock

SERVER_PORT = 65500
BUFFER_SIZE = 2048
lock = Lock()
class ClientListener(Thread):
    def __init__(self, name: str, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock
        self.name = name 

    def run(self):
        filename = self.sock.recv(BUFFER_SIZE).decode() 
        filename = os.path.basename(filename)
        self.sock.send("1".encode()) 
        filesize = int(self.sock.recv(BUFFER_SIZE).decode())
        with lock: 
            if filename in os.listdir('.'): 
                i = 1
                dot_split = filename.split('.')
                name, ext = dot_split[0], ".".join(dot_split[1:]) 
                while(filename in os.listdir('.')):
                    filename = name + "("+str(i)+")." + ext
                    i += 1
                
            f = open(filename, "wb")
            f.close()
        with open(filename, "wb") as f:
            for i in range(math.ceil(filesize/BUFFER_SIZE)):
                f.write(self.sock.recv(BUFFER_SIZE))
                self.sock.send("1".encode())
        self.sock.close()


def main():
    next_name = 1
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', SERVER_PORT))
    sock.listen()
    while True:
        client_socket, address = sock.accept() 
        name = 'user ' + str(next_name)
        next_name += 1
        print(str(address), name)
        ClientListener(name, client_socket).start()

if __name__ == "__main__":
    main()

