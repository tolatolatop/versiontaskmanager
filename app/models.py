from sqlalchemy import Column, String, TIMESTAMP
import uuid
from .database import Base


class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    task_name = Column(String, index=True)
    status = Column(String, index=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
