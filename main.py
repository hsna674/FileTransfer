import socket


def send_data():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = input("Enter the server IP adress: ")
    filePath = input("Enter the path of the file the you want to send: ")
    fileName, fileType = input("Enter the name of the file you want to send (Include the file type!): ").split(".")

    port = 38573

    client.connect((host, port))

    with open(filePath, "r") as f:
        client.sendall((f.read() + "$#filesignature#$" + fileName + "$#filesignature#$" + fileType).encode())

    client.close()


def receive_data():
    ipSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ipSocket.connect(("8.8.8.8", 80))
    hostIP = ipSocket.getsockname()[0]
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 38573

    server.bind((hostIP, port))
    server.listen()

    print(f"Server listening on {hostIP}:{port}")

    client, clientAddr = server.accept()
    print(f"Connection from {clientAddr}")

    fileData, fileName, fileType = client.recv(1024).decode().split("$#filesignature#$")

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
