from db_connection import get_connection, release_connection

#ADD USER INFORMATION TO THE DATABASE
def add_user(add_username, add_password):
    conn = get_connection()
    cur = conn.cursor()

    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cur.execute (query, (add_username, add_password))
    conn.commit()

    release_connection()


#AUTHENTICATE THE USER'S IDENTITY
def authenticate_user(auth_username, auth_password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute ("SELECT username FROM users")
    name =  cur.fetchone()
    cur.execute ("SELECT password FROM users")
    passw = cur.fetchone()

    if name == auth_username and passw == auth_password:
        add_user(auth_username, auth_password)
        print ("You are successfully logged in!")
        print (f"Welcome back {auth_username}")
    else:
        print("Incorrect username or password! ")
        print("Sorry, we couldn't log you in! ")

    release_connection()


#SHOW ONLINE USERS
def show_online_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT username FROM users WHERE online_status = true")
    online_users = cur.fetchall()
    for users in online_users:
        print (users)

    release_connection()


#SHOW ALL REGISTERED USERS
def show_all_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute ("SELECT username, online_status, last_seen FROM users")
    all_users = cur.fetchall()
    for users in all_users:
        print (users)

    release_connection()