from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import uuid

app = FastAPI()

DATABASE = "data/shorturl.db"

class URLShortenRequest(BaseModel):
    url: str

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.on_event("startup")
def startup():
    conn = get_db_connection()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS urls (id TEXT PRIMARY KEY, full_url TEXT)"
    )
    conn.commit()
    conn.close()

@app.post("/shorten")
def shorten_url(request: URLShortenRequest):
    short_id = str(uuid.uuid4())[:8]
    conn = get_db_connection()
    conn.execute("INSERT INTO urls (id, full_url) VALUES (?, ?)", (short_id, request.url))
    conn.commit()
    conn.close()
    return {"short_id": short_id}

@app.get("/{short_id}")
def redirect_url(short_id: str):
    conn = get_db_connection()
    url = conn.execute("SELECT full_url FROM urls WHERE id = ?", (short_id,)).fetchone()
    conn.close()
    if url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"url": url["full_url"]}

@app.get("/stats/{short_id}")
def get_url_stats(short_id: str):
    conn = get_db_connection()
    url = conn.execute("SELECT * FROM urls WHERE id = ?", (short_id,)).fetchone()
    conn.close()
    if url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"short_id": url["id"], "full_url": url["full_url"]}
