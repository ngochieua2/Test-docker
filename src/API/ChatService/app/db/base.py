# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.chat_thread import ChatThread  # noqa
from app.models.chat_message import ChatMessage  # noqa