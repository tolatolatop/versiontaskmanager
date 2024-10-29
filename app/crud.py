import uuid
from sqlalchemy.orm import Session
from . import models, schemas
import datetime


def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(
        task_name=task.task_name,
        status="待执行",
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Task).offset(skip).limit(limit).all()


def get_task(db: Session, task_id: uuid.UUID):
    return db.query(models.Task).filter(models.Task.task_id == task_id).first()
