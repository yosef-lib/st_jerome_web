import sqlite3

conn = sqlite3.connect('katalog.db')
cursor = conn.cursor()
cursor.execute('SELECT lokasi, COUNT(*) FROM buku GROUP BY lokasi;')
for row in cursor.fetchall():
    print(row)
conn.close()
