from app.memory.conversation_manager import ConversationManager


class SessionManager:

    def __init__(self):
        self.sessions = {}

    def get_session(
        self,
        session_id: str
    ) -> ConversationManager:

        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationManager()

        return self.sessions[session_id]

    def clear_session(self, session_id: str):

        if session_id in self.sessions:
            del self.sessions[session_id]