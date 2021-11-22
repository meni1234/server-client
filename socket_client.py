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
    SOCK.send(b"DOWNLOAD")
    SOCK.send(file_name.encode())
    
    file_size = struct.unpack("i", SOCK.recv(4))[0]

    with open(file_name + '(copy)', "wb") as f:        
                
        bytes_= 0
        print('Downloading...')
        while bytes_< file_size:
            l = SOCK.recv(BUFFER_SIZE)
            f.write(l)
            bytes_ += 1024
   
        print(f'Successfully downloaded {file_name}')

    return

   
def get_list():
    
    SOCK.send(b"LIST")
    file_size = struct.unpack("i", SOCK.recv(4))[0]

    with open('list of files.txt', 'wb') as list_files:

        bytes_= 0
        while bytes_< file_size:
            l = SOCK.recv(BUFFER_SIZE)
            list_files.write(l)
            bytes_ += 1024
  


def main():

    print('OPTIONS:\n'
          '       CONNECT-----------------------------connect to server\n'
          '       UPLOAD <path_of_your_file>------upload file on server\n'
          '       DOWNLOAD <file_name>--------download file from server\n'
          '       LIST-------------------list all files exist on server\n'
          '       END----------------------------------------------exit')
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

