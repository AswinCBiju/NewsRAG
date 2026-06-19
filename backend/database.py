import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="newsrag",
        user="postgres",
        password=os.getenv("DB_PASSWORD")
    )
    return conn

def save_article(title, source, url, published_at, content):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO articles (title, source, url, published_at, content)
        VALUES (%s, %s, %s, %s, %s)
    """, (title, source, url, published_at, content))
    conn.commit()
    cur.close()
    conn.close()
    