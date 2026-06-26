import sqlite3

from db import cursor, conn

DB_NAME = "todo.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        todo text not null,
        time text not null
    )""")


    conn.commit()
    conn.close()



def add_todo(todo, time):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""insert into todos(todo, time) values (?, ?)""",
                   (todo, time))
    conn.commit()
    conn.close()


def get_todos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""select * from todos""")
    todos = cursor.fetchall()
    conn.close()
    return todos


if __name__ == "__main__":

    for todo in get_todos():
        print(str(todo[0]))