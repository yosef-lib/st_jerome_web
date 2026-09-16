import sqlite3
conn = sqlite3.connect('katalog.db')
rows = conn.execute("SELECT no_induk, judul, klasifikasi FROM buku WHERE no_induk IN ('8129/22', '8132/22')").fetchall()
for r in rows:
    print(r)
