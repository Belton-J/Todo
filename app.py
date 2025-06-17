import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="ToDo App", layout="centered")
st.title("✅ My ToDo List")
st.markdown("---")

# --- Add Task ---
with st.container():
    st.subheader("➕ Add a Task")
    cols = st.columns([5, 1])
    new_task = cols[0].text_input("New Task", placeholder="e.g., Finish homework", label_visibility="collapsed")
    if cols[1].button("Add", use_container_width=True):
        if new_task.strip():
            res = requests.post(f"{API_URL}/tasks", json={"text": new_task})
            if res.status_code == 200:
                st.success("Task added successfully!")
                time.sleep(0.5)
                st.rerun()
            else:
                try:
                    error_detail = res.json().get("detail", "Something went wrong.")
                    st.error(f"Error: {error_detail}")
                except Exception:
                    st.error("Unexpected error occurred.")
        else:
            st.warning("Please enter a task.")

st.markdown("---")

# --- Load Tasks ---
try:
    response = requests.get(f"{API_URL}/tasks")
    tasks = response.json().get("list", [])
except:
    st.error("Could not connect to the API.")
    st.stop()

# --- Display Tasks ---
st.subheader("📋 Your Tasks")
if not tasks:
    st.info("🎉 No tasks yet. Add one above!")
else:
    with st.container():
        for task in tasks:
            task_id = task["id"]
            task_text = task["text"]
            task_status = task["status"]

            # Create a row for each task
            cols = st.columns([0.5, 6, 1, 1])

            # --- Complete/Incomplete Checkbox ---
            is_checked = cols[0].checkbox("", value=task_status, key=f"cb_{task_id}")
            if is_checked != task_status:
                # Toggle status
                requests.put(f"{API_URL}/tasks/complete/{task_id}")
                st.rerun()

            # --- Task Text (disabled or editable) ---
            if f"edit_{task_id}" in st.session_state:
                new_text = cols[1].text_input(
                    label="Edit Task",
                    value=task_text,
                    label_visibility="collapsed",
                    key=f"text_{task_id}",
                )
                if cols[2].button("💾", key=f"save_{task_id}"):
                    requests.put(f"{API_URL}/tasks", json={"id": task_id, "text": new_text, "status": task_status})
                    del st.session_state[f"edit_{task_id}"]
                    st.rerun()
                if cols[3].button("✖", key=f"cancel_{task_id}"):
                    del st.session_state[f"edit_{task_id}"]
            else:
                style = "color: gray;" if task_status else ""
                cols[1].markdown(f"<div style='{style}'>{task_text}</div>", unsafe_allow_html=True)
                if cols[2].button("✏️", key=f"editbtn_{task_id}"):
                    st.session_state[f"edit_{task_id}"] = True
                    st.rerun()
                if cols[3].button("🗑️", key=f"del_{task_id}"):
                    requests.delete(f"{API_URL}/tasks/{task_id}")
                    st.success("Task deleted.")
                    time.sleep(0.5)
                    st.rerun()

            