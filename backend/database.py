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
    
def get_cached_articles(topic, hours_limit=24):
    """Checks the database for recent articles matching the topic."""
    conn = get_connection()
    cur = conn.cursor()
    
    # We use ILIKE for case-insensitive matching (e.g., matches "GTA 6" or "gta 6")
    # We also check that the article was saved within the last X hours
    cur.execute("""
        SELECT title, source, url, published_at, content 
        FROM articles 
        WHERE (title ILIKE %s OR content ILIKE %s)
        AND saved_at >= NOW() - INTERVAL '%s hours'
        ORDER BY published_at DESC
        LIMIT 5;
    """, (f"%{topic}%", f"%{topic}%", hours_limit))
    
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    return rows