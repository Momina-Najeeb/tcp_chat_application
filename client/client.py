import socket

client = socket.socket()
try:
    client.connect(("localhost", 5555))
except:
    print ("Error connecting the server! ")
    exit()
print(client.recv(1024).decode())    


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
        break

    else:
        print("Enter a valid choice!")


choice2 = input (""" Choose 1, 2, 3, 4:
                 1. Show Online Users
                 2. Show all users
                 3. Chat
                 4. Exit
                 """)

if choice2 == "1":
    client.send("SHOW_ONLINE_USERS".encode())
    response = client.recv(1024).decode()
    print("Online Users:")
    print(response)

elif choice2 == "2":
    client.send("SHOW_ALL_USERS")
    response = client.recv(1024).decode()
    print("All registered users:\n")
    print(response)

if choice2 == "3":
    client.send("CHAT".encode())
    client.send(username)
    recipient = input("Enter recipient username: ")
    client.send(recipient.encode())
    message = input("Enter your message: ")
    client.send(message.encode())
    print("Message sent!")


    




client.close()