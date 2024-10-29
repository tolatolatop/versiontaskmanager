from pydantic import BaseModel
import uuid
from datetime import datetime


class TaskBase(BaseModel):
    task_name: str


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    task_id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
