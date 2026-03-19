import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('''
CREATE TABLE IF NOT EXISTS volunteers(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
phone TEXT
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS donations(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
amount INTEGER
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS contacts(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
message TEXT
)
''')

conn.close()

print("Database created successfully")