import sqlite3
import sys

def safe_migrate():
    conn = sqlite3.connect('katalog.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reservasi'")
        if not cursor.fetchone():
            print("Tabel reservasi belum ada, membuat baru...")
            cursor.execute('''
                CREATE TABLE reservasi (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    member_id TEXT NOT NULL,
                    biblio_id INTEGER NOT NULL,
                    tanggal_reservasi DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'MENUNGGU'
                )
            ''')
            conn.commit()
            return
            
        # If table exists, check columns
        cursor.execute("PRAGMA table_info(reservasi)")
        columns = [row['name'] for row in cursor.fetchall()]
        
        added = False
        if 'member_id' not in columns:
            print("Menambahkan kolom member_id...")
            cursor.execute("ALTER TABLE reservasi ADD COLUMN member_id TEXT DEFAULT ''")
            added = True
            
        if 'biblio_id' not in columns:
            print("Menambahkan kolom biblio_id...")
            cursor.execute("ALTER TABLE reservasi ADD COLUMN biblio_id INTEGER DEFAULT 0")
            added = True
            
        if 'status' not in columns:
            print("Menambahkan kolom status...")
            cursor.execute("ALTER TABLE reservasi ADD COLUMN status TEXT DEFAULT 'MENUNGGU'")
            added = True
            
        if 'tanggal_reservasi' not in columns:
            print("Menambahkan kolom tanggal_reservasi...")
            cursor.execute("ALTER TABLE reservasi ADD COLUMN tanggal_reservasi DATETIME DEFAULT CURRENT_TIMESTAMP")
            added = True
            
        if added:
            conn.commit()
            print("Migrasi aman selesai! Kolom yang kurang berhasil ditambahkan tanpa menghapus data.")
        else:
            print("Tabel reservasi sudah lengkap, tidak ada yang perlu diubah.")
            
    except Exception as e:
        print("Error saat migrasi:", e)
    finally:
        conn.close()

if __name__ == '__main__':
    safe_migrate()
