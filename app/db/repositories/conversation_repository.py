from sqlalchemy.orm import Session

from app.db.models import Conversation


class ConversationRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_session_id(
        self,
        session_id: str,
    ) -> Conversation | None:

        return (
            self.db.query(Conversation)
            .filter(
                Conversation.session_id
                == session_id
            )
            .first()
        )

    def create(
        self,
        session_id: str,
    ) -> Conversation:

        conversation = Conversation(
            session_id=session_id,
        )

        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def get_or_create(
        self,
        session_id: str,
    ) -> Conversation:

        conversation = self.get_by_session_id(
            session_id
        )

        if conversation is not None:
            return conversation

        return self.create(
            session_id
        )

    def delete(
        self,
        session_id: str,
    ) -> None:

        conversation = self.get_by_session_id(
            session_id
        )

        if conversation is not None:
            self.db.delete(conversation)
            self.db.commit()