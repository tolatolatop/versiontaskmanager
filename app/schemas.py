from pydantic import BaseModel
import uuid
from datetime import datetime


class TaskBase(BaseModel):
    task_name: str


class TaskCreate(TaskBase):
    pass


class TaskUpdateStatus(BaseModel):
    status: str


class Task(TaskBase):
    task_id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
