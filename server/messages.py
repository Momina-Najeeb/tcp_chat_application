from db_connection import get_connection, release_connection

#SAVE THE MESSAGES OF USERS
def save_message(sender_id, receiver_id, message):
    conn = get_connection()
    cur = conn.cursor()

    query = "INSERT INTO messages (sender_id, recipient_id, message_content) VALUES (%s, %s, %s)"
    cur.execute(query, (sender_id, receiver_id, message))
    conn.commit()

    cur.close()
    release_connection()


#SHOW MY INBOX
def show_inbox(inbox_username):
    conn = get_connection()
    cur = conn.cursor()
 
    query ="""
        SELECT sender.username, m.content 
        FROM messages m 
        JOIN users sender ON m.sender_id = sender.id 
        JOIN users recipient ON m.recipient_id = recipient.id
        WHERE recipient.username = %s
        """
    cur.execute(query, (inbox_username,))
    my_inbox = cur.fetchall()
    for row in my_inbox:
        print(row[0], ": ", row[1])

    cur.close()
    release_connection()
