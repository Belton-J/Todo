from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app=FastAPI()
TasksList=[]


class Task(BaseModel):
    id: int
    text:str
    status:bool


@app.post("/tasks")
async def addTask(task:Task):
    TasksList.append(task)
    return {"msg":"Task Added Successfully"}


@app.get("/tasks")
async def getTask():
    if TasksList:
        return {"list":TasksList}
    else:
        return{"msg":"The list is empty"}


@app.delete("/tasks/{number}")
async def deleteTask(number:int):
    for i,tsk in enumerate(TasksList):
        if tsk.id==number:
            TasksList.pop(i)
            return {"msg": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task Not Found")


@app.put("/tasks")
async def puttext(etask:Task):
    for i in TasksList:
        if i.id==etask.id:
            i.text=etask.text
            return {"msg":"Task Changed Successfully"}
    raise HTTPException(status_code=404,detail="Task Not Found")

@app.put("/tasks/complete/{number}")
async def comtext(number:int):
    for i in TasksList:
        if i.id==number:
            i.status=True
            return {"msg":"Task Completed"}
    raise HTTPException(status_code=404,detail="Task Not Found")

    