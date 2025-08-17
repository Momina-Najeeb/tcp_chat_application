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
client.close()