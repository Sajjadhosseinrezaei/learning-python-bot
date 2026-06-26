import sqlite3

DB_NAME = "taskmanager.db"


def init_db():
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()


    table_creation_query = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        status TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        chat_id INTEGER NOT NULL
    );
    """
    cursor.execute(table_creation_query)
    connect.commit()
    cursor.close()
    connect.close()



def create_task(title, status, user_id, chat_id):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()

    try:
        with connect:
            cursor.execute(
                "INSERT INTO tasks (title, status, user_id, chat_id) VALUES (?, ?, ?, ?);",
                (title, status, user_id, chat_id),
            )
            print("تراکنش موفقیت آمیز بود")
    except sqlite3.Error as e:
        print(f" خطایی رخ داده است\n{e}")

    finally:
        cursor.close()
        connect.close()



def retrieve_tasks(chat_id):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    tasks = []
    try:
        query = "SELECT * FROM tasks WHERE chat_id = ?;"
        cursor.execute(query, (chat_id,))
        tasks = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"خطایی در خواندن داده‌ها رخ داد\n{e}")
    finally:
        cursor.close()
        connect.close()
    return tasks



def update_task(id, title, status):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    try:
        with connect:
            query = """
            UPDATE tasks
            SET title = ?, status = ?
            WHERE id = ?;
            """
            cursor.execute(query, (title, status, id))
    except sqlite3.Error as e:
        print(f"خطایی رخ داد \n{e}")

    finally:
        cursor.close()
        connect.close()


def delete_task(id):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    try:
        with connect:
            query = """
            DELETE FROM tasks
            WHERE id = ?;
            """
            cursor.execute(query, (id,))
    except sqlite3.Error as e:
        print(f"خطایی رخ داد \n{e}")

    finally:
        cursor.close()
        connect.close()