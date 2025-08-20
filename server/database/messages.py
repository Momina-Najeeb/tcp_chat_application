from .db_connection import get_connection, release_connection

#SAVE THE MESSAGES OF USERS
def save_message(sender_id, receiver_id, message):
    conn = get_connection()
    cur = conn.cursor()
    try:
        query = "INSERT INTO messages (sender_id, recipient_id, message_content) VALUES (%s, %s, %s)"
        cur.execute(query, (sender_id, receiver_id, message))
        conn.commit()
    except Exception as e:
        print(f"Error saving message: {e}")
    finally:
        cur.close()
        release_connection(conn)


#SHOW MY INBOX
def show_inbox(inbox_username):
    conn = get_connection()
    cur = conn.cursor()
    try:
        query = """
            SELECT sender.username, m.message_content 
            FROM messages m
            JOIN users sender ON m.sender_id = sender.id 
            JOIN users recipient ON m.recipient_id = recipient.id
            WHERE recipient.username = %s
            """
        cur.execute(query, (inbox_username,))
        my_inbox = cur.fetchall()
        return my_inbox  
    except Exception as e:
        print(f"Error showing inbox: {e}")
        return []
    finally:
        cur.close()
        release_connection(conn)
