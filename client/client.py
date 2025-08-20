import socket
import sys

def connect_to_server(host, port):
    client = socket.socket()
    try:
        client.connect((host, port))
    except:
        print("Error connecting to the server!")
        exit()
    print(client.recv(1024).decode())
    return client


def authentication(client):
    while True:
        choice = input("""Choose: 1, 2, or 3
                    1: LOGIN
                    2: SIGNUP
                    3: EXIT
                    Your choice: """
        )
        if choice == "1":
            client.send("LOGIN".encode())
            username = input("Enter your username: ")
            client.send(username.encode())
            password = input("Enter password: ")
            client.send(password.encode())
            response = client.recv(1024).decode()
            print(response)
            if "Login successful" in response:
                break
            elif "Login unsuccessful" in response:
                continue

        elif choice == "2":
            client.send("SIGNUP".encode())
            username = input("Enter your username: ")
            client.send(username.encode())
            password = input("Enter password: ")
            client.send(password.encode())
            response = client.recv(1024).decode()
            print(response)
            if "Signup successful" in response:
                break
            elif "Username already in use" in response:
                print("Try a different username: ")
                continue

        elif choice == "3":
            client.send("EXIT".encode())
            print("Exiting...")
            client.close()
            break

        else:
            print("Enter a valid choice!")

def main_menu(client):
    while True:
        menu_option = input (""" Choose 1, 2, 3, 4, 5:
                        1. Show Online Users
                        2. Show all users
                        3. Search user by their username
                        4. Show my inbox
                        5. Exit
                        Your choice: """
        )

        if menu_option == "1":
            client.send("SHOW_ONLINE_USERS".encode())
            response = client.recv(1024).decode()
            online_users = response.strip().split('\n')
            if not online_users or online_users == ['']:
                print("No users online.")
                input("Press Enter to go back to main menu...")
                continue
            print("Online Users:")
            for idx, user in enumerate(online_users, 1):
                print(f"{idx}. {user}")
            while True:
                action = input("Select a user to chat with (number) or 'b' to go back: ")
                if action.lower() == 'b':
                    break
                try:
                    selection = int(action)
                    recipient = online_users[selection - 1]
                except (ValueError, IndexError):
                    print("Invalid selection.")
                    continue
                client.send("CHAT".encode())
                client.send(recipient.encode())
                message = input(f"Enter your message to {recipient}: ")
                client.send(message.encode())
                confirm = client.recv(1024).decode()
                print(confirm)
                input("Press Enter to go back to main menu...")
                break

        elif menu_option == "2":
            client.send("SHOW_ALL_USERS".encode())
            response = client.recv(1024).decode()
            all_users = response.strip().split('\n')
            if not all_users or all_users == ['']:
                print("No users found.")
                input("Press Enter to go back to main menu...")
                continue
            print("All Registered Users:")
            for idx, user in enumerate(all_users, 1):
                print(f"{idx}. {user}")
            while True:
                action = input("Select a user to chat with (number) or 'b' to go back: ")
                if action.lower() == 'b':
                    break
                try:
                    selection = int(action)
                    recipient = all_users[selection - 1]
                except (ValueError, IndexError):
                    print("Invalid selection.")
                    continue
                client.send("CHAT".encode())
                client.send(recipient.encode())
                message = input(f"Enter your message to {recipient}: ")
                client.send(message.encode())
                confirm = client.recv(1024).decode()
                print(confirm)
                input("Press Enter to go back to main menu...")
                break

        elif menu_option == "3":
            client.send("SEARCH_USER".encode())
            search_name = input("Enter the username to search: ")
            client.send(search_name.encode())
            response = client.recv(1024).decode()
            if response.strip() == "":
                print("User not found.")
            else:
                print("User Info:")
                print(response)
            input("Press Enter to go back to main menu...")

        elif menu_option == "4":
            client.send("SHOW_INBOX".encode())
            response = client.recv(4096).decode()
            if not response.strip():
                print("Your inbox is empty.")
            else:
                print("Your Inbox:")
                print(response)
            input("Press Enter to go back to main menu...")

        elif menu_option == "5":
            client.send("EXIT".encode())
            print("Exiting...")
            client.close()
            break

        else:
            print("Invalid choice! Please try again.")




if len(sys.argv) > 2:
    host = sys.argv[1]
    port = int(sys.argv[2])
else:
    host = "localhost"
    port = 5555

client = connect_to_server(host, port)
authentication(client)
main_menu(client)

client.close()