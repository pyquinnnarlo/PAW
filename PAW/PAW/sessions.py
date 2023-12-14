import sqlite3
import uuid

class Session:
    @classmethod
    def create_session(cls, user_id):
        session_id = str(uuid.uuid4())
        conn = sqlite3.connect('sessions.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sessions (session_id, user_id) VALUES (?, ?)', (session_id, user_id))
        conn.commit()
        conn.close()
        return session_id

    @classmethod
    def delete_session(cls, session_id):
        conn = sqlite3.connect('sessions.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
        conn.commit()
        conn.close()

    @classmethod
    def get_user_id(cls, session_id):
        conn = sqlite3.connect('sessions.db')
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM sessions WHERE session_id = ?', (session_id,))
        user_id = cursor.fetchone()
        conn.close()
        return user_id[0] if user_id else None
