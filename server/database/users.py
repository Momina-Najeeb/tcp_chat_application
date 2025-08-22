from .db_connection import get_connection, release_connection

#ADD USER INFORMATION TO THE DATABASE
def add_user(add_username, add_password):
    conn = get_connection()
    cur = conn.cursor()
    query1 = "SELECT 1 FROM users WHERE username = %s"
    cur.execute (query1, (add_username, ))
    if cur.fetchone():
        return "Username already in use!\n Please enter another"
        
    else:
        query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
        cur.execute (query, (add_username, add_password))
        conn.commit()
        release_connection(conn)
        return f"Signup successful! Welcome {add_username}"


#AUTHENTICATE THE USER'S IDENTITY
def authenticate_user(auth_username, auth_password):
    conn = get_connection()
    cur = conn.cursor()

    query = "SELECT password_hash FROM users WHERE username = %s"
    cur.execute (query, (auth_username, ))
    row = cur.fetchone()
    release_connection(conn)
    if row and row[0] == auth_password:
        return f"Login successful! \nWelcome back {auth_username}"
    else:
        return "Login unsuccessful! Incorrect username or password! "



#SHOW ONLINE USERS
def show_online_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT username FROM users WHERE online_status = true")
    online_users = cur.fetchall()
    release_connection(conn)
    if online_users:
        return online_users
    else:
        return []


#SHOW ALL REGISTERED USERS
def show_all_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute ("SELECT username, online_status, last_seen FROM users")
    all_users = cur.fetchall()
    release_connection(conn)
    if all_users:
        return all_users
    else:
        return []


#GET USER ID FROM THE DATABASE
def get_user_id(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    result = cur.fetchone()
    release_connection(conn)
    if result:
        return result[0]
    else:
        None


#UPDTAE USER ONLINE STATUS
def update_user_online_status(username, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET online_status = %s WHERE username = %s", (status, username))
    conn.commit()
    release_connection(conn)


    #GET USER LAST SEEN TIME
def update_user_last_seen(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET last_seen = NOW() WHERE username = %s", (username,))
    conn.commit()
    release_connection(conn)


#GET USER INFO
def get_user_info(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT username, online_status, last_seen FROM users WHERE username = %s", (username,))
    result = cur.fetchone()
    release_connection(conn)
    return result