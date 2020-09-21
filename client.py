import sys
import socket
import os
import math

from tqdm import tqdm

BUFFER_SIZE = 2048
file_name = sys.argv[1]
domain = sys.argv[2]
port = int(sys.argv[3])
filesize = os.path.getsize(file_name)
s = socket.socket()
s.connect((domain, port))
s.send(file_name.encode())
_ = s.recv(BUFFER_SIZE)
s.send(str(filesize).encode())
progress = tqdm(range(filesize), unit_divisor=2048)
with open(file_name, "rb") as f:
    for i in range(math.ceil(filesize/BUFFER_SIZE)):
        bytes_read = f.read(BUFFER_SIZE)
        s.sendall(bytes_read)
        progress.update(len(bytes_read))
s.close()