from sqlalchemy.orm import Session

from app.db.repositories.conversation_repository import (
    ConversationRepository,
)
from app.db.repositories.message_repository import (
    MessageRepository,
)


class ConversationService:

    def __init__(self, db: Session):
        self.conversation_repository = (
            ConversationRepository(db)
        )
        self.message_repository = (
            MessageRepository(db)
        )

    def get_or_create_conversation(
        self,
        session_id: str,
    ):
        return self.conversation_repository.get_or_create(
            session_id
        )

    def add_message(
        self,
        conversation_id: int,
        role: str,
        content: str,
    ):
        return self.message_repository.create(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

    def get_history(
        self,
        conversation_id: int,
    ) -> list[dict]:

        messages = self.message_repository.get_messages(
            conversation_id
        )

        return [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in messages
        ]

    def clear_conversation(
        self,
        session_id: str,
    ) -> None:

        conversation = (
            self.conversation_repository.get_by_session_id(
                session_id
            )
        )

        if conversation is None:
            return

        self.message_repository.delete_messages(
            conversation.id
        )