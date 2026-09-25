import sqlite3
conn = sqlite3.connect('katalog.db')
try:
    conn.execute("ALTER TABLE sjla_visitor_logs ADD COLUMN fakultas TEXT")
    print("Added fakultas column")
except Exception as e:
    print(e)
conn.commit()
conn.close()
