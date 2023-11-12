import os
import utilities

# Assigning host and port through utilities
HOST = utilities.HOST
PORT = utilities.PORT

def handle_client(sock, addr):
    try:
        # Fetch encryption mode
        data = utilities.recv_msg(sock)

        # No encryption required for plain text
        if data == "1":
            # Receive the command
            msg = utilities.recv_msg(sock)
            print('{}: {}'.format(addr, msg))
            print("Received message: " + msg)
            tokens = msg.split()

            # 5 conditions for 5 commands
            if msg.lower() == "cwd":
                output = utilities.curr_dir()
                utilities.send_msg(sock, output)

            if msg.lower() == "ls":
                path = utilities.curr_dir()
                output = str(utilities.ls(path))
                utilities.send_msg(sock, output)

            if msg.split(" ")[0].lower() == "cd":
                path = msg.split(" ")[1]
                for i in range(2, len(msg.split(" "))):
                    path += " " + msg.split(" ")[i]

                if path in os.listdir() or path == '..':
                    output = utilities.change_dir(path)
                    utilities.send_msg(sock, output)
                else:
                    output = "No such directory exists!"
                    utilities.send_msg(sock, output)

            if msg.split(" ")[0].lower() == "dwd":
                filename = tokens[1]
                for i in range(2, len(tokens)):
                    filename += " " + tokens[i]
                # Read characters, encode with 'utf-8', and send as bytes using sendall
                with open(filename, 'r') as f:
                    while True:
                        data = f.read(1024)
                        if not data:
                            break
                        data = data.encode('utf-8')
                        sock.sendall(data)
                    f.close()
                # Prompt client if the download is completed
                msg = "Download Completed!"
                utilities.send_msg(sock, msg)

            if msg.split(" ")[0].lower() == "upd":
                filename = tokens[1]
                for i in range(2, len(tokens)):
                    filename += " " + tokens[i]
                # Receive as bytes, decode to characters, and write as a string
                with open(filename, 'w') as f:
                    while True:
                        data = sock.recv(1024).decode()
                        if not data:
                            f.close()
                            break
                        f.write(data)
                        # Receive in packets of 1024, in the last iteration when less than 1024, write that data, then close the file to avoid the prompt being written in the file itself
                        if len(data) < 1024:
                            f.close()
                            break
                # Prompt client if the upload is completed
                msg = "Upload Completed!"
                utilities.send_msg(sock, msg)

        # Mode is Substitute, encrypt before sending, decrypt after receiving
        elif data == "2":

            msg = utilities.recv_msg(sock)
            msg = utilities.decrypt_sub(msg)
            print('{}: {}'.format(addr, msg))
            print("Received message: " + msg)
            tokens = msg.split()
            if msg.lower() == "cwd":
                output = utilities.curr_dir()
                utilities.send_msg(sock, utilities.encrypt_sub(output))

            if msg.lower() == "ls":
                path = utilities.curr_dir()
                output = str(utilities.ls(path))
                utilities.send_msg(sock, utilities.encrypt_sub(output))
            if msg.split(" ")[0].lower() == "cd":
                path = msg.split(" ")[1]
                for i in range(2, len(msg.split(" "))):
                    path += " " + msg.split(" ")[i]

                if path in os.listdir() or path == '..':
                    output = utilities.change_dir(path)
                    utilities.send_msg(
                        sock, utilities.encrypt_sub(output))
                else:
                    output = "No such directory exists!"
                    utilities.send_msg(
                        sock, utilities.encrypt_sub(output))

            if msg.split(" ")[0].lower() == "dwd":
                filename = tokens[1]
                for i in range(2, len(tokens)):
                    filename += " " + tokens[i]

                with open(filename, 'r') as f:
                    while True:
                        data = f.read(1024)
                        if not data:
                            break
                        data = utilities.encrypt_sub(data)
                        data = data.encode('utf-8')
                        sock.sendall(data)
                    f.close()
                msg = "Download Completed!"
                utilities.send_msg(sock, utilities.encrypt_sub(msg))

            if msg.split(" ")[0].lower() == "upd":
                filename = tokens[1]
                for i in range(2, len(tokens)):
                    filename += " " + tokens[i]
                with open(filename, 'w') as f:
                    while True:
                        data = sock.recv(1024).decode()
                        data = utilities.decrypt_sub(data)
                        if not data:
                            f.close()
                            break
                        f.write(data)
                        if len(data) < 1024:
                            f.close()
                            break

                msg = "Upload Completed!"
                utilities.send_msg(sock, utilities.encrypt_sub(msg))

        # Mode is transpose, reverse the message before sending and after receiving
        elif data == "3":

            msg = utilities.recv_msg(sock)
            msg = utilities.transpose(msg)
            print('{}: {}'.format(addr, msg))
            print("Received message: " + msg)
            tokens = msg.split()

            if msg.lower() == "cwd":
                output = utilities.curr_dir()
                utilities.send_msg(sock, utilities.transpose(output))

            if msg.lower() == "ls":
                path = utilities.curr_dir()
                output = str(utilities.ls(path))
                utilities.send_msg(sock, utilities.transpose(output))
            if msg.split(" ")[0].lower() == "cd":
                path = msg.split(" ")[1]
                for i in range(2, len(msg.split(" "))):
                    path += " " + msg.split(" ")[i]

                if path in os.listdir() or path == '..':
                    output = utilities.change_dir(path)
                    utilities.send_msg(
                        sock, utilities.transpose(output))
                else:
                    output = "No such directory exists!"
                    utilities.send_msg(
                        sock, utilities.transpose(output))

            if msg.split(" ")[0].lower() == "dwd":
                filename = tokens[1]
                for i in range(2, len(tokens)):
                    filename += " " + tokens[i]

                with open(filename, 'r') as f:
                    while True:
                        data = f.read(1024)
                        if not data:
                            f.close()
                            break
                        data = utilities.transpose(data)
                        data = data.encode('utf-8')
                        sock.sendall(data)

                msg = "Download Completed!"
                utilities.send_msg(sock, utilities.transpose(msg))

            if msg.split(" ")[0].lower() == "upd":
                filename = tokens[1]
                for i in range(2, len(tokens)):
                    filename += " " + tokens[i]
                with open(filename, 'w') as f:
                    while True:
                        data = sock.recv(1024).decode()
                        data = utilities.transpose(data)
                        if not data:
                            f.close()
                            break
                        f.write(data)
                        if len(data) < 1024:
                            f.close()
                            break

                msg = "Upload Completed!"
                utilities.send_msg(sock, utilities.transpose(msg))
        # If the user gives a number other than 1, 2, or 3, the server prints "Invalid Number!"
        else:
            print("Invalid number!")
    # Except block for handling errors and printing them as Socket Error
    except (ConnectionError, BrokenPipeError):
        print('Socket Error')
    finally:
        print('Closed connection to {}'.format(addr))
        sock.close()

if __name__ == '__main__':
    # Create a listening socket
    listen_sock = utilities.create_listen_socket(HOST, PORT)
    addr = listen_sock.getsockname()
    print('Listening on {}'.format(addr))
    # Main while loop of the server
    while True:
        # Accept client connections
        client_sock, addr = listen_sock.accept()
        print('Connection from {}'.format(addr))
        # Handle the client in a separate function
        handle_client(client_sock, addr)
