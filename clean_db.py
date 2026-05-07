import sqlite3

conn = sqlite3.connect("resume.db")
cursor = conn.cursor()

# Check existing columns
cursor.execute("PRAGMA table_info(users)")
columns = [col[1] for col in cursor.fetchall()]

print("Existing columns:", columns)

# Create new clean table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users_new (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Case 1: email exists
if "email" in columns:
    cursor.execute("""
    INSERT INTO users_new (id, username, email, password)
    SELECT id, username, email, password
    FROM users
    WHERE email IS NOT NULL
    """)
else:
    # Case 2: email does NOT exist → generate dummy emails
    cursor.execute("""
    INSERT INTO users_new (id, username, email, password)
    SELECT id, username, username || '@temp.com', password
    FROM users
    """)

# Replace old table
cursor.execute("DROP TABLE users")
cursor.execute("ALTER TABLE users_new RENAME TO users")

conn.commit()
conn.close()

print("Database cleaned successfully!")