from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uuid
from sql import get_tasks, add_task, delete_task, update_task, complete_task

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class Task(BaseModel):
    id: str
    text: str
    status: bool

class CreateTask(BaseModel):
    text: str

@app.get("/tasks")
def read_tasks():
    tasks = get_tasks()
    if tasks:
        return {"list": tasks}
    else:
        raise HTTPException(status_code=404,detail="No Task Found")

@app.post("/tasks")
def create_task(item: CreateTask):
    task_id = str(uuid.uuid4())
    success = add_task(task_id, item.text, False)
    if success:
        return {"msg": "Task created."}
    raise HTTPException(status_code=500, detail="Task creation failed.")

@app.delete("/tasks/{task_id}")
def delete(task_id: str):
    if delete_task(task_id):
        return {"msg": "Task deleted successfully."}
    raise HTTPException(status_code=404, detail="Task not found.")

@app.put("/tasks")
def update(item: Task):
    if update_task(item.id, item.text):
        return {"msg": "Task updated."}
    raise HTTPException(status_code=404, detail="Task not found.")

@app.put("/tasks/complete/{task_id}")
def complete(task_id: str):
    if complete_task(task_id):
        return {"msg": "Task status toggled."}
    raise HTTPException(status_code=404, detail="Task not found.")
