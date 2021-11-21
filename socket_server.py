import socket
import struct


SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
BUFFER_SIZE = 1024


def connection():
    SOCK.bind(('127.0.0.1', 55555))
    SOCK.listen()
    conn, addr = SOCK.accept()
         
    return conn


def save(conn, file_name, file_size):

    with open(file_name + '(copy)', "wb") as f:

        bytes_= 0
        print('Recieving...')
        while bytes_< file_size:
            l = conn.recv(BUFFER_SIZE)
            f.write(l)
            bytes_ += 1024
    return



if __name__== "__main__":

    conn = connection()
    command = conn.recv(BUFFER_SIZE).decode()
    #file_name = conn.recv(BUFFER_SIZE).decode().split('.')

    if command == 'UPLOAD':
        file_size = struct.unpack("i", conn.recv(4))[0]
        file_name = conn.recv(BUFFER_SIZE).decode()

        save(conn, file_name, file_size)
         

