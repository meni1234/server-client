import socket
import sys
import struct

if sys.argv[1] == 'ip':
    HOST = sys.argv[2]
else:
    HOST = '127.0.0.1'

PORT = 55555        # The port used by the server
BUFFER_SIZE = 1024
SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connection():

    try:
        SOCK.connect((HOST, PORT))
        print('Connection sucessful')
    except:
        print('Connection unsucessful. Make sure the server is online.')
    

def upload(file_name):
    
    print(f'Uploading file: {file_name}...')
    SOCK.send(b'UPLOAD')    

    with open(file_name, "rb") as content:

        SOCK.send(struct.pack("i", len(file_name))) 
        SOCK.send(file_name.encode())
        try:
            l = content.read(BUFFER_SIZE)
            print("Sending...")
            while l:
                SOCK.send(l)
                l = content.read(BUFFER_SIZE)
        except:
            print('Error sending file')
    return
    

def download(file_name):

    print(f'Downloading file: {file_name}')
    SOCK.send("DOWNLOAD")
    SOCK.send(file_name)
    SOCK.recv(BUFFER_SIZE)
    file_size = struct.unpack("i", s.recv(4))[0]
    
    with open(file_name, "wb") as f:
        bytes_recieved = 0
        print('Downloading...')
        while bytes_recieved < file_size:
            l = s.recv(BUFFER_SIZE)
            f.write(l)
            bytes_recieved += BUFFER_SIZE
        
        print(f'Successfully downloaded {file_name}')

    return




    

def main():

    print('OPTIONS:\n'
          '       CONNECT-----------------------------connect to server\n'
          '       UPLOAD <path_of_your_file>------upload file on server\n'
          '       DOWNLOAD <file_name>--------download file from server\n'
          '       LIST-------------------list all files exist on server')
    prompt = input("Enter a command: ")
    if prompt == "CONNECT":
        connection()
        command = input("Enter a command: ")
        if command[:6] == "UPLOAD":
            upload(command[7:])
        elif command[:8] == "DOWNLOAD":
            download(command[9:])
        elif command[:4] == "LIST":
            get_list()



if __name__ == "__main__":
    main() 

