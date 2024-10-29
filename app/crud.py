import logging
from sqlalchemy.orm import Session
from . import models, schemas
import datetime


def time_record(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        logging.warning(f"Function {func.__name__} executed in {end_time - start_time}")
        return result

    return wrapper


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


@time_record
def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Task).offset(skip).limit(limit).all()


def get_task(db: Session, task_id: str):
    return db.query(models.Task).filter(models.Task.task_id == task_id).first()


def update_task_status(db: Session, task_id: str, status: str):
    task = db.query(models.Task).filter(models.Task.task_id == task_id).first()
    if task:
        task.status = status
        task.updated_at = datetime.datetime.now()
        db.commit()
        db.refresh(task)
    return task
