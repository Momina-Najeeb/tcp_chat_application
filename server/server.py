import socket
import threading
import sys
from database.users import authenticate_user, add_user, show_online_users, show_all_users, get_user_id, update_user_online_status, get_user_info
from database.messages import save_message, show_inbox

def start_server(host, port):
    new_server = socket.socket()
    new_server.bind((host, port))
    return new_server

if len(sys.argv) > 2:
    host = sys.argv[1]
    port = int(sys.argv[2])
else:
    host = "localhost"
    port = 5555

server = start_server(host, port)
server.listen(5)
print(f"Server started on {host}:{port}")


def send_message(client, message):
    client.send(message.encode())

online_clients = {}
clients = []
names = []

def handle_client(client, address):
        print(f"Connection established with {address}")
        client.send("You are connected to your server".encode())
    
        logged_in = False
        username = None
        
        while not logged_in:
            auth = client.recv(1024).decode()
            
            if auth == "LOGIN":
                username = client.recv(1024).decode()
                password = client.recv(1024).decode()
                print("Logging the client in...")
                result = authenticate_user(username, password)
                client.send(result.encode())
                if "Login successful" in result:
                     logged_in = True
                     update_user_online_status(username, True)
                     print(f"{username} logged in successfully!")
                     online_clients[username] = client
                     break
                
            elif auth == "SIGNUP":
                username = client.recv(1024).decode()
                password = client.recv(1024).decode()
                print("Signing up the client...")
                result = add_user(username, password)
                client.send(result.encode())
                if "Signup successful" in result:
                     logged_in = True
                     update_user_online_status(username, True)
                     print(f"{username} signed up successfully!")
                     online_clients[username] = client
                     break
                
            elif auth == "EXIT":
                print (f"client address {address} disconnected!")
                client.close()
                break

        while logged_in:

            choice = client.recv(1024).decode()
            if choice == "SHOW_ONLINE_USERS":
                        print("Showing online users...")
                        users = show_online_users()
                        user_list = "\n".join([u[0] for u in users])
                        client.send(user_list.encode())
                        if client.recv(1024).decode() == "CHAT":
                            print("Client wants to chat...")
                            recipient = client.recv(1024).decode()
                            message = client.recv(1024).decode()
                            sender_id = get_user_id(username)
                            receiver_id = get_user_id(recipient)

                            if recipient in online_clients:
                                try:
                                    send_message(online_clients[recipient], f"{username}: {message}")
                                    save_message(sender_id, receiver_id, message)
                                except Exception as e:
                                    print(f"{e}: Message delivery failed to {recipient}")
                                    client.send(f"Failed to deliver message to {recipient}.".encode())
                                else:
                                    client.send("Message delivered!".encode())
                            else:
                                save_message(sender_id, receiver_id, message)
                                client.send("Message delivered!".encode())
                             
            elif choice == "SHOW_ALL_USERS":
                print("Showing all registered users...")
                users = show_all_users()
                user_list = "\n".join([u[0] for u in users])
                client.send(user_list.encode())
            elif choice == "CHAT":
                print("Client wants to chat...")
                recipient = client.recv(1024).decode()
                message = client.recv(1024).decode()
                sender_id = get_user_id(username)
                receiver_id = get_user_id(recipient)
                save_message(sender_id, receiver_id, message)
                if recipient in online_clients:
                     send_message(online_clients[recipient], f"{username}: {message}")
                client.send("Message delivered!".encode())

            elif choice == "SEARCH_USER":
                search_name = client.recv(1024).decode()
                user_info = get_user_info(search_name)  # You need to implement this function
                if user_info:
                    username, online_status, last_seen = user_info
                    status = "Online" if online_status else f"Offline (last seen: {last_seen})"
                    client.send(f"{username} - {status}".encode())
                else:
                    client.send("".encode())

            elif choice == "SHOW_INBOX":
                print(f"Showing inbox for {username}...")
                inbox = show_inbox(username)  # Should return a list of (sender, message) tuples
                if inbox:
                    inbox_str = "\n".join([f"{sender}: {msg}" for sender, msg in inbox])
                    client.send(inbox_str.encode())
                else:
                    client.send("".encode())
            elif choice == "EXIT":
                print(f"{username} has disconnected.")
                update_user_online_status(username, False)
                client.close()
                logged_in = False
                break

while True:
    client, address = server.accept()
    thread = threading.Thread(target=handle_client, args=(client, address))
    thread.start()