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


def send_file(conn, file_name):

    with open(file_name, "rb") as f:
        
        try:
            part = f.read(BUFFER_SIZE)
            print("Sending...")
            while part:
                conn.send(part)
                part = f.read(BUFFER_SIZE)
        except:
            print('Error sending file')
    return


def save_list(file_name):
    
    with open('list.txt', 'a') as l:
            l.write(f'\n{file_name}')


def send_list(conn):
    
    with open('list.txt', "rb") as f:
        conn.send(struct.pack("i", len('list.txt')))
        try:
            part = f.read(BUFFER_SIZE)
            print("Sending...")
            while part:
                conn.send(part)
                part = f.read(BUFFER_SIZE)
        except:
            print('Error sending list')
    return


if __name__== "__main__":

    conn = connection()
    command = conn.recv(BUFFER_SIZE).decode()
 
    if command == 'UPLOAD':
        file_size = struct.unpack("i", conn.recv(4))[0]
        file_name = conn.recv(BUFFER_SIZE).decode()
        save(conn, file_name, file_size)
        save_list(file_name)

    if command == 'DOWNLOAD':
        file_name = conn.recv(BUFFER_SIZE).decode()
        conn.send(struct.pack("i", len(file_name)))
        send_file(conn, file_name)       
               
    if command == 'LIST':
       
        send_list(conn)
        
