import sqlite3



def create_tasks(title):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO tasks VALUES (?,?)""",(None,title))
    conn.commit()
    conn.close()

def update_tasks(id, title):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE tasks SET title=? WHERE id=?" , (title, id))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect("tasks.db")

    cursor = conn.cursor()

    cursor.execute("SELECT id, title FROM  tasks")

    tasks = cursor.fetchall()

    conn.close()

    return tasks




