import socket
import utilities
import sys
import timeit

HOST = '10.0.0.4'  # IP of Mininet host
PORT = utilities.PORT

# Function to handle the download process
def handle_download(sock, msg, encryption_func, decode_func, extension):
    begin = timeit.default_timer()
    utilities.send_msg(sock, encryption_func(msg))
    filename = msg.split()[1:]
    filename = " ".join(filename)
    
    with open(filename, 'w') as f:
        while True:
            data = sock.recv(1024).decode()
            data = decode_func(data)
            if not data:
                break
            f.write(data)
            if len(data) < 1024:
                break
    
    f.close()
    msg = utilities.recv_msg(sock)
    msg = decode_func(msg)
    end = timeit.default_timer()
    interval = round((end - begin), 3)
    print(msg)
    print(f"Time taken for download: {interval}s")

# Function to handle the upload process
def handle_upload(sock, msg, encryption_func, encode_func):
    begin = timeit.default_timer()
    utilities.send_msg(sock, encryption_func(msg))
    filename = msg.split()[1:]
    filename = " ".join(filename)

    with open(filename, 'r') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            data = encryption_func(data)
            data = data.encode('utf-8')
            sock.sendall(data)
    
    f.close()
    msg = utilities.recv_msg(sock)
    msg = encryption_func(msg)
    end = timeit.default_timer()
    interval = round((end - begin), 3)
    print(msg)
    print(f"Time taken for upload: {interval}s")

# Function to handle other commands
def handle_other_commands(sock, msg, encryption_func, decode_func):
    utilities.send_msg(sock, encryption_func(msg))
    print('Sent message: {}'.format(msg))
    msg = utilities.recv_msg(sock)
    msg = decode_func(msg)
    print('Received echo: ' + msg)

if __name__ == '__main__':
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            print('\nConnected to {}:{}'.format(HOST, PORT))

            data = input("Select any number from 1, 2, and 3: ")
            utilities.send_msg(sock, data)

            if data in ["1", "2", "3"]:
                print("Type message, enter to send, 'exit' to quit")
                msg = input()
                tokens = msg.split()

                if msg == 'exit':
                    print("Connection closed!")
                    break
                elif tokens[0] in ["dwd", "upd"]:
                    if data == "1":
                        handle_download(sock, msg, lambda x: x, lambda x: x, "")
                    elif data == "2":
                        handle_download(sock, msg, utilities.encrypt_sub, utilities.decrypt_sub, "")
                    elif data == "3":
                        handle_download(sock, msg, utilities.transpose, utilities.transpose, "")
                else:
                    if data == "1":
                        handle_other_commands(sock, msg, lambda x: x, lambda x: x)
                    elif data == "2":
                        handle_other_commands(sock, msg, utilities.encrypt_sub, utilities.decrypt_sub)
                    elif data == "3":
                        handle_other_commands(sock, msg, utilities.transpose, utilities.transpose)
            else:
                print("Please select a valid number!")

        except ConnectionError:
            print('Socket error')
            sock.close()
            break

        finally:
            sock.close()
            print('Closed connection to server\n')
