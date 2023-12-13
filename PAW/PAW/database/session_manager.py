import secrets
from datetime import datetime, timedelta

class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self):
        session_id = secrets.token_hex(16)
        self.sessions[session_id] = {"created_at": datetime.now()}
        return session_id

    def get_session_data(self, session_id):
        return self.sessions.get(session_id, {}).get("data", {})

    def set_session_data(self, session_id, data):
        self.sessions[session_id]["data"] = data

    def delete_expired_sessions(self, max_session_age_minutes=30):
        current_time = datetime.now()
        expired_sessions = [session_id for session_id, session_data in self.sessions.items()
                            if (current_time - session_data["created_at"]).total_seconds() / 60 > max_session_age_minutes]

        for session_id in expired_sessions:
            del self.sessions[session_id]
            
    def remove_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]
