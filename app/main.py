from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Task API",
    description="Petite API REST pour pratiquer les bases du DevOps.",
    version="1.0.0",
)

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=500)

class Task(TaskCreate):
    id: int
    completed: bool = False

# Stockage en mémoire : les tâches seront perdues au redémarrage.
tasks: dict[int, Task] = {}
next_id = 1

@app.get("/")
def root():
    return {"message": "Bienvenue sur Task API", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks", response_model=list[Task])
def list_tasks():
    return list(tasks.values())

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate):
    global next_id
    task = Task(id=next_id, title=payload.title, description=payload.description)
    tasks[next_id] = task
    next_id += 1
    return task

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Tâche introuvable")
    return task

@app.patch("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: int):
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Tâche introuvable")
    updated = task.model_copy(update={"completed": True})
    tasks[task_id] = updated
    return updated

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Tâche introuvable")
    del tasks[task_id]
