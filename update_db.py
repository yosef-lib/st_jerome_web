import sqlite3
conn = sqlite3.connect('katalog.db')
try:
    conn.execute("ALTER TABLE sjla_visitor_logs ADD COLUMN peran_jabatan TEXT")
    print("Added peran_jabatan")
except:
    print("Column already exists")
conn.commit()
conn.close()
