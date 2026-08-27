from app.db.database import Base, SessionLocal, engine
from app.db.repositories.conversation_repository import (
    ConversationRepository,
)
from app.db.repositories.message_repository import (
    MessageRepository,
)


def test_conversation_persistence():

    db = SessionLocal()

    try:
        conversation_repository = (
            ConversationRepository(db)
        )

        message_repository = MessageRepository(db)

        conversation = (
            conversation_repository.get_or_create(
                "pytest-session"
            )
        )

        message_repository.create(
            conversation.id,
            "user",
            "Hello from pytest",
        )

        message_repository.create(
            conversation.id,
            "assistant",
            "Hello!",
        )

        messages = (
            message_repository.get_messages(
                conversation.id
            )
        )

        assert len(messages) >= 2

        assert messages[-2].role == "user"
        assert (
            messages[-2].content
            == "Hello from pytest"
        )

        assert messages[-1].role == "assistant"
        assert (
            messages[-1].content
            == "Hello!"
        )

    finally:
        db.close()