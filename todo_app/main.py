from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI()

DATABASE = "data/todo.db"

class TodoItem(BaseModel):
    id: int  # Добавлено поле id
    title: str
    description: str = None
    completed: bool = False

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.on_event("startup")
def startup():
    conn = get_db_connection()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT, completed BOOLEAN)"
    )
    conn.commit()
    conn.close()

@app.post("/items/", response_model=TodoItem)
def create_item(item: TodoItem):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (title, description, completed) VALUES (?, ?, ?)",
                   (item.title, item.description, item.completed))
    conn.commit()
    item_id = cursor.lastrowid  # Получаем последний сгенерированный id
    conn.close()
    return {**item.dict(), "id": item_id}  # Возвращаем элемент с id

@app.get("/items/", response_model=List[TodoItem])
def read_items():
    conn = get_db_connection()
    items = conn.execute("SELECT * FROM items").fetchall()
    conn.close()
    return [dict(item) for item in items]

@app.get("/items/{item_id}", response_model=TodoItem)
def read_item(item_id: int):
    conn = get_db_connection()
    item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    conn.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return dict(item)

@app.put("/items/{item_id}", response_model=TodoItem)
def update_item(item_id: int, item: TodoItem):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET title = ?, description = ?, completed = ? WHERE id = ?",
                   (item.title, item.description, item.completed, item_id))
    conn.commit()
    conn.close()
    return {**item.dict(), "id": item_id}  # Возвращаем элемент с id

@app.delete("/items/{item_id}", response_model=dict)
def delete_item(item_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return {"message": "Item deleted"}

@app.delete("/items/", response_model=dict)
def delete_all_items():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items")
    conn.commit()
    conn.close()
    return {"message": "All items deleted"}
