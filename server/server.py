import socket
from users import authenticate_user, add_user, show_online_users, show_all_users, get_user_id, update_user_online_status
from messages import save_message
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

        logged_in = False
        username = None
        
        while not logged_in:
            choice = client.recv(1024).decode()
            
            if choice == "LOGIN":
                username = client.recv(1024).decode()
                password = client.recv(1024).decode()
                print("Logging the client in...")
                result = authenticate_user(username, password)
                client.send(result.encode())
                if "Login successful" in result:
                     logged_in = True
                     update_user_online_status(username, True)
                     print(f"{username} logged in successfully!")
                     break
                
            elif choice == "SIGNUP":
                username = client.recv(1024).decode()
                password = client.recv(1024).decode()
                print("Signing up the client...")
                result = add_user(username, password)
                client.send(result.encode())
                if "Signup successful" in result:
                     logged_in = True
                     update_user_online_status(username, True)
                     print(f"{username} signed up successfully!")
                     break
                
            elif choice == "EXIT":
                print (f"client address {address} disconnected!")
                client.close()
                break

        while logged_in:

            client.recv(1024).decode()
            if choice == "SHOW_ONLINE_USERS":
                        print("Showing online users...")
                        users = show_online_users()
                        user_list = "\n".join([u[0] for u in users])
                        client.send(user_list.encode())
            elif choice == "SHOW_ALL_USERS":
                print("Showing all registered users...")
                users = show_all_users()
                user_list = "\n".join([u[0] for u in users])
                client.send(user_list.encode())
            elif choice == "CHAT":
                print("Client wants to chat...")
                sender = client.recv(1024).decode()
                recipient = client.recv(1024).decode()
                message = client.recv(1024).decode()
                sender_id = get_user_id(sender)
                receiver_id = get_user_id(recipient)
                save_message(sender_id, receiver_id, message)
                client.send("Message delivered!".encode())
            elif choice == "EXIT":
                print(f"{username} has disconnected.")
                update_user_online_status(username, False)
                client.close()
                logged_in = False
                break
                

            


