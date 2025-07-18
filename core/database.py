import sqlite3

DB_NAME = 'data/users.db'

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

def get_cursor():
    return cursor

def commit_db():
    conn.commit()

def close_db():
    conn.close()

# Initialize tables if not exist
def init_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        mobile TEXT,
        email TEXT UNIQUE,
        password TEXT,
        nid_path TEXT,
        bank_card_path TEXT,
        is_verified INTEGER DEFAULT 0
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        receiver TEXT,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        user_email TEXT,
        contact_email TEXT,
        UNIQUE(user_email, contact_email)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY,
        password TEXT
    )
    ''')
    conn.commit()

init_db()
