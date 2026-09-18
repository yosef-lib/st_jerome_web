import sqlite3

def force_migration():
    conn = sqlite3.connect('katalog.db')
    cursor = conn.cursor()
    
    # 1. Create bibliografi
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bibliografi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        judul TEXT NOT NULL,
        gmd TEXT DEFAULT 'Text',
        edisi TEXT,
        isbn TEXT,
        penerbit TEXT,
        tahun_terbit TEXT,
        deskripsi_fisik TEXT,
        judul_seri TEXT,
        klasifikasi TEXT,
        cutter TEXT,
        huruf_judul TEXT,
        bahasa TEXT DEFAULT 'Indonesia',
        tempat_terbit TEXT,
        pengarang TEXT,
        subjek TEXT,
        image TEXT
    )
    ''')

    # 2. Create eksemplar
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS eksemplar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        biblio_id INTEGER NOT NULL,
        no_induk TEXT UNIQUE NOT NULL,
        status_buku TEXT DEFAULT 'BELI',
        lokasi TEXT DEFAULT 'IMAVI',
        tgl_terima TEXT,
        copy_ke INTEGER DEFAULT 1,
        catatan TEXT,
        status_ketersediaan TEXT DEFAULT 'Tersedia',
        FOREIGN KEY (biblio_id) REFERENCES bibliografi(id)
    )
    ''')
    
    # Create sirkulasi table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sirkulasi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id TEXT NOT NULL,
        no_induk TEXT NOT NULL,
        loan_date TEXT NOT NULL,
        due_date TEXT NOT NULL,
        return_date TEXT,
        renewal_count INTEGER DEFAULT 0,
        fine_amount INTEGER DEFAULT 0,
        fine_status TEXT DEFAULT 'BELUM_LUNAS'
    )
    ''')
    
    # Try migrating data if eksemplar is empty
    cursor.execute("SELECT COUNT(*) FROM eksemplar")
    if cursor.fetchone()[0] == 0:
        try:
            cursor.execute("SELECT * FROM buku")
            buku_rows = cursor.fetchall()
            cursor.execute("PRAGMA table_info(buku)")
            columns = [col[1] for col in cursor.fetchall()]
            
            migrated_count = 0
            for row in buku_rows:
                row_dict = dict(zip(columns, row))
                
                cursor.execute('''
                    INSERT INTO bibliografi (
                        judul, gmd, edisi, isbn, penerbit, tahun_terbit, deskripsi_fisik, 
                        judul_seri, klasifikasi, cutter, huruf_judul, bahasa, tempat_terbit, 
                        pengarang, subjek
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row_dict.get('judul'), row_dict.get('gmd'), row_dict.get('edisi'), 
                    row_dict.get('isbn'), row_dict.get('penerbit'), row_dict.get('tahun_terbit'), 
                    row_dict.get('deskripsi_fisik'), row_dict.get('judul_seri'), 
                    row_dict.get('klasifikasi'), row_dict.get('cutter'), row_dict.get('huruf_judul'), 
                    row_dict.get('bahasa'), row_dict.get('tempat_terbit'), row_dict.get('pengarang'), 
                    row_dict.get('subjek')
                ))
                biblio_id = cursor.lastrowid
                
                cursor.execute('''
                    INSERT INTO eksemplar (
                        biblio_id, no_induk, status_buku, lokasi, tgl_terima, copy_ke, catatan
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    biblio_id, row_dict.get('no_induk'), row_dict.get('status_buku'), 
                    row_dict.get('lokasi'), row_dict.get('tgl_terima'), row_dict.get('copy_ke'), 
                    row_dict.get('catatan')
                ))
                migrated_count += 1
            print(f"Migrated {migrated_count} records.")
        except Exception as e:
            print(f"Error migrating: {e}")
    else:
        print("Data already exists in eksemplar, skipping migration.")
        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    force_migration()
