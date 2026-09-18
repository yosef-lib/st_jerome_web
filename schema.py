import sqlite3

conn = sqlite3.connect('katalog.db')
cursor = conn.cursor()
cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
for row in cursor.fetchall():
    if row[0] in ['buku', 'anggota', 'loans', 'peminjaman']:
        print(f"Table: {row[0]}")
        print(row[1])
conn.close()
