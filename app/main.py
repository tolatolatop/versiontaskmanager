from fastapi import FastAPI, Depends, Request, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from . import models, schemas, crud
from .database import SessionLocal, engine
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)


@app.get("/tasks/", response_model=list[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks


@app.get("/tasks/{task_id}")
async def read_task(task_id: str, request: Request, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id=task_id)
    if task is None:
        return {"error": "任务未找到"}
    return templates.TemplateResponse(
        "task_detail.html", {"request": request, "task": task}
    )


@app.websocket("/tasks/{task_id}/logs/ws")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await websocket.accept()
    log_path = f"logs/{task_id}.log"
    try:
        with open(log_path, "r") as log_file:
            while True:
                line = log_file.readline()
                if line:
                    await websocket.send_text(line)
    except WebSocketDisconnect:
        print(f"WebSocket for task {task_id} disconnected")


@app.get("/")
async def read_root(request: Request, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db)
    return templates.TemplateResponse(
        "index.html", {"request": request, "tasks": tasks}
    )
