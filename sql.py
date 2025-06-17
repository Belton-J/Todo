import sqlite3

def connect():
    conn = sqlite3.connect("todo.db", check_same_thread=False)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            text TEXT NOT NULL,
            status BOOLEAN NOT NULL
        )
    """)
    conn.commit()
    return conn

conn = connect()
cursor = conn.cursor()

def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    data = cursor.fetchall()
    return [{"id": row[0], "text": row[1], "status": bool(row[2])} for row in data]

def add_task(id, text, status):
    try:
        cursor.execute("INSERT INTO tasks (id, text, status) VALUES (?, ?, ?)", (id, text, status))
        conn.commit()
        return True
    except:
        return False

def delete_task(id):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    return cursor.rowcount > 0

def update_task(id, text):
    cursor.execute("UPDATE tasks SET text = ? WHERE id = ?", (text, id))
    conn.commit()
    return cursor.rowcount > 0

def complete_task(id):
    cursor.execute("SELECT status FROM tasks WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        return False
    new_status = not bool(row[0])
    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, id))
    conn.commit()
    return True
