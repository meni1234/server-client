import socket
import sys


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
    
    SOCK.recv(BUFFER_SIZE)
    SOCK.send(file_name)
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



if __name__ == "__main__":
    
    print('OPTIONS:\nCONNECT------connect to server.\nUPLOAD------upload <path_of_your_file>/\nDOWNLOAD <file_name>')
    prompt = input("Enter a command: ")
    if prompt == "CONNECT":
        connection()
        prompt = input("Enter a command: ")
        if prompt == "UPLOAD":
            upload(prompt[1])
        elif prompt == "DOWNLOAD":
            download(prompt[1])

#    file_name = '/home/meni/meni/yosi.txt'

