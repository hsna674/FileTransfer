import sys
sys.dont_write_bytecode = True

import socket
from constants import *


def send_data():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = input("Enter the server IP adress: ")
    filePath = input("Enter the path of the file the you want to send: ")

    try:
        fileName, fileType = input(
                "Enter the name of the file you want to send (Include the file type!): "
                ).split(".")
    except ValueError:
        print("Make sure that your input only contains exactly one period!")
        quit()

    client.connect((host, PORT))

    with open(filePath, "r") as f:
        client.sendall((f.read() + FILE_SIGNATURE
                        + fileName + FILE_SIGNATURE
                        + fileType).encode())

    client.close()


def receive_data():
    ipSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ipSocket.connect(("8.8.8.8", 80))
    hostIP = ipSocket.getsockname()[0]
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((hostIP, PORT))
    server.listen()

    print(f"Server listening on {hostIP}:{PORT}")

    client, clientAddr = server.accept()
    print(f"Connection from {clientAddr}")

    fileData, fileName, fileType = client.recv(1024).decode().split(
            FILE_SIGNATURE
            )

    with open(fileName + "." + fileType, "w") as f:
        f.write(fileData)


def main():
    print("1. Send Data")
    print("2. Receive Data")

    choice = input("Choose 1 or 2: ")

    if choice == '1':
        send_data()
    elif choice == '2':
        receive_data()
    else:
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
