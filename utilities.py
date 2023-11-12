import socket
import os

# User defined IP address for the HOST and PORT IS 4040
HOST = ''
PORT = 4040

# Creates a listening socket [taken from the book]
def create_listen_socket(host, port):
    # Setup the sockets our server will receive connection requests on
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(100)
    return sock

# Receives a message from any end through a byte array [taken from the book]
def recv_msg(sock):
    # Wait for data to arrive on the socket, then parse into messages using b'\0' as message delimiter
    data = bytearray()
    msg = ''
    while not msg:
        recvd = sock.recv(4096)
        if not recvd:
            # Socket has been closed prematurely
            raise ConnectionError()
        data = data + recvd
        if b'\0' in recvd:
            # we know from our protocol rules that we only send
            # one message per connection, so b'\0' will always be
            # the last character
            msg = data.rstrip(b'\0')
            break

    msg = msg.decode('utf-8')
    return msg

# Adds a null byte at the end of the message which helps us in receiving and sending the message
# and where to end [taken from the book]
def prep_msg(msg):
    # Prepare a string to be sent as a message
    msg += '\0'
    return msg.encode('utf-8')

# Sends a string over a socket, preparing it first [taken from the book]
def send_msg(sock, msg):
    data = prep_msg(msg)
    sock.sendall(data)

def curr_dir():
    # Get the current working directory using os library
    return os.getcwd()

def ls(p1):
    # Gets the list if files in path 'p1'
    return os.listdir(p1)

def change_dir(p2):
    # Changes the current directory to p2
    os.chdir(p2)
    return os.getcwd()

# Referred online for this function
def encrypt_sub(msg):
    encrypted = ""
    # Took the offset to be 2
    offset = 2

    for i in range(len(msg)):
        char = msg[i]
        # If it is alphanumeric then this works otherwise just append the character
        if(char.isalnum()):
            # Encrypting upper case letters
            if(char.isupper()):
                encrypted += chr((ord(char) - 65 + offset) % 26 + 65)
            # Encrypting lower case letters
            elif(char.islower()):
                encrypted += chr((ord(char) - 97 + offset) % 26 + 97)
            # Encrypting numbers
            else:
                encrypted += chr((ord(char) - 48 + offset) % 10 + 48)
        else:
            encrypted += char

    return encrypted

def decrypt_sub(msg):
    decrypted = ""
    # In decryption offset will be negative of 2, everything else remains the same
    offset = -2
    for i in range(len(msg)):
        char = msg[i]
        if(char.isalnum()):
            if(char.isupper()):
                decrypted += chr((ord(char) - 65 + offset) % 26 + 65)
            elif(char.islower()):
                decrypted += chr((ord(char) - 97 + offset) % 26 + 97)
            else:
                decrypted += chr((ord(char) - 48 + offset) % 10 + 48)
        else:
            decrypted += char

    return decrypted

# Encryption and decryption in transpose are the same
# Reversing the string word by word using space as a delimiter
def transpose(msg):
    reversed = ""
    words = msg.split()
    for i in range(len(words)):
        words[i] = words[i][::-1]

    for i in range(len(words) - 1):
        reversed = reversed + words[i] + " "

    reversed += words[len(words) - 1]

    return reversed
