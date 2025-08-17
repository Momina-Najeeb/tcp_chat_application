import socket
from users import authenticate_user, add_user
server = socket.socket()

server.bind(("localhost", 5555))
server.listen(5)
print("Server waiting for requests")


connection_confirmation = "You are connected to your server \nPress c to continue: "



clients = []
names = []

while True:
    
        client, address = server.accept()
        print(f"Connection established with {address}")
        client.send("You are connected to your server".encode())
        
        while True:
            choice = client.recv(1024).decode()
            

            if choice == "LOGIN":
                username = client.recv(1024).decode()
                password = client.recv(1024).decode()
                print("Logging the client in...")
                result = authenticate_user(username, password)
                client.send(result.encode())
            elif choice == "SIGNUP":
                username = client.recv(1024).decode()
                password = client.recv(1024).decode()
                print("Signing up the client...")
                result = add_user(username, password)
                client.send(result.encode())
            elif choice == "EXIT":
                print (f"client address {address} disconnected!")
                client.close()
                break

