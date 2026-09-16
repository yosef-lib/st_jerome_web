import sqlite3

conn = sqlite3.connect('katalog.db')
conn.execute('''
CREATE TABLE IF NOT EXISTS sjla_visitor_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    waktu_kunjungan DATETIME DEFAULT CURRENT_TIMESTAMP,
    tipe_pengunjung TEXT,
    identitas TEXT,
    asal_instansi TEXT,
    tujuan_kunjungan TEXT
)
''')
conn.commit()
conn.close()
print("Table sjla_visitor_logs created successfully.")
