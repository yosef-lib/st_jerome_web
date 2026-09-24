import sqlite3

def fix_table():
    conn = sqlite3.connect('katalog.db')
    try:
        conn.execute('DROP TABLE IF EXISTS reservasi')
        conn.execute('''
            CREATE TABLE reservasi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id TEXT NOT NULL,
                biblio_id INTEGER NOT NULL,
                tanggal_reservasi DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'MENUNGGU'
            )
        ''')
        conn.commit()
        print("Tabel reservasi berhasil diperbaiki!")
    except Exception as e:
        print("Gagal:", e)
    finally:
        conn.close()

if __name__ == '__main__':
    fix_table()
