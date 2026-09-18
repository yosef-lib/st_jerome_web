import sqlite3

def migrate():
    conn = sqlite3.connect('katalog.db')
    c = conn.cursor()
    
    # 1. Tabel Usulan Buku
    c.execute('''
    CREATE TABLE IF NOT EXISTS usulan_buku (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        judul_topik TEXT NOT NULL,
        pengarang TEXT,
        catatan TEXT,
        tanggal DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'Menunggu'
    )
    ''')
    
    # 2. Tabel Pencarian Gagal (Unmet Search Queries)
    c.execute('''
    CREATE TABLE IF NOT EXISTS pencarian_gagal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT NOT NULL UNIQUE,
        jumlah_pencarian INTEGER DEFAULT 1,
        update_terakhir DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 3. Tabel Reservasi
    c.execute('''
    CREATE TABLE IF NOT EXISTS reservasi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        biblio_id INTEGER NOT NULL,
        nim_pemustaka TEXT NOT NULL,
        tanggal DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'Aktif',
        FOREIGN KEY (biblio_id) REFERENCES bibliografi (id)
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Migrasi tabel OPAC berhasil.")

if __name__ == '__main__':
    migrate()
