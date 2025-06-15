import streamlit as st
import requests

if "count" not in st.session_state:
    st.session_state.count = 0

if "task_added" not in st.session_state:
    st.session_state.task_added = False

API_URL="http://127.0.0.1:8000"

st.title("ToDo List")

#To Create Task
txt=st.text_area(label="Enter your action here",placeholder="Eg. Wake up at 5 am",key="CreateTask")
def to_post(text_data):
    data={
        "id":st.session_state.count+1,
        "text":text_data,
        "status":False
    }
    res=requests.post(f"{API_URL}/tasks",json=data)
    if res.status_code==200:
        st.session_state.count+=1
        st.session_state.task_added = True
        

st.button(label="Add",on_click=to_post,args=(txt,),key="addbutton")
if st.session_state.task_added:
    st.success("Task Added Successfully")
    st.session_state.task_added = False


#TO PRINT ToDo TASKS
st.header("Tasks")
res=requests.get(f"{API_URL}/tasks")
if res.json().get("list") is None:
    st.success(res.json().get("msg"))
else:
    tlist=res.json().get("list")

    for i,tsk in enumerate(tlist):
        st.text_area(label=f"Task {tsk['id']}",value=f"{tsk['text']}",disabled=True,key=f"listedTask{i}")


#TO PRINT Completed TASKS
st.header("Completed Tasks")
res=requests.get(f"{API_URL}/tasks")
if res.json().get("list") is None:
    st.success(res.json().get("msg"))
else:
    tlist=res.json().get("list")

    for i,tsk in enumerate(tlist):
        if tsk['status']==True:
            st.text_area(label=f"Task {tsk['id']}",value=f"{tsk['text']}",disabled=True,key=f"CompletedTask{i}")



#To Delete a task
st.header("Delete Task")
dtask=st.number_input(label="Enter the Task ID",placeholder="Enter the task ID to Remove the Task",step=1)
delbut=st.button(label="Delete")
if delbut:
    res = requests.delete(f"{API_URL}/tasks/{int(dtask)}")
    if res.status_code == 200:
        st.success(res.json().get("msg"))
    else:
        st.warning(res.json().get("detail"))



#TO Edit a Task

st.header("Edit Task")
dtask=st.number_input(label="Enter the Task ID",placeholder="Enter the task ID to Edit the Task",step=1)
edittext=st.text_area(label="Edit the Task",placeholder="Make Changes Here")
editdic={
    "id":int(dtask),
    "text":edittext,
    "status":False
}
chgbut=st.button(label="Make Changes")
if chgbut:
    res = requests.put(f"{API_URL}/tasks",json=editdic)
    if res.status_code == 200:
        st.success(res.json().get("msg"))
    else:
        st.warning(res.json().get("detail"))


#To complete Task
st.header("Complete the Task")
ctask=st.number_input(label="Enter the Task ID",placeholder="Enter the task ID to Complete the Task",step=1)
combut=st.button(label="Complete")
if combut:
    res = requests.put(f"{API_URL}/tasks/complete/{int(ctask)}")
    if res.status_code == 200:
        st.success(res.json().get("msg"))
    else:
        st.warning(res.json().get("detail"))


            