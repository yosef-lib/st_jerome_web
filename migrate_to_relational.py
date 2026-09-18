import sqlite3

def migrate():
    conn = sqlite3.connect('katalog.db')
    cursor = conn.cursor()
    
    # 1. Create Bibliografi table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bibliografi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        judul TEXT NOT NULL,
        pengarang TEXT,
        pernyataan_tanggungjawab TEXT,
        edisi TEXT,
        info_detail_spesifik TEXT,
        gmd TEXT,
        tipe_isi TEXT,
        tipe_media TEXT,
        tipe_pembawa TEXT,
        kala_terbit TEXT,
        isbn TEXT,
        penerbit TEXT,
        tahun_terbit TEXT,
        tempat_terbit TEXT,
        deskripsi_fisik TEXT,
        judul_seri TEXT,
        klasifikasi TEXT,
        no_panggil TEXT,
        subjek TEXT,
        bahasa TEXT DEFAULT 'Indonesia',
        abstrak TEXT,
        gambar_sampul TEXT,
        lampiran TEXT
    )
    ''')

    # 2. Create Eksemplar table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS eksemplar (
        no_induk TEXT PRIMARY KEY,
        biblio_id INTEGER,
        lokasi TEXT DEFAULT 'IMAVI',
        status_buku TEXT DEFAULT 'TERSEDIA',
        copy_ke INTEGER DEFAULT 1,
        is_reference_only INTEGER DEFAULT 0,
        tgl_terima TEXT,
        FOREIGN KEY(biblio_id) REFERENCES bibliografi(id) ON DELETE CASCADE
    )
    ''')
    
    # 3. Check if we need to migrate existing 'buku' data
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='buku'")
    if cursor.fetchone():
        cursor.execute("SELECT * FROM buku")
        books = cursor.fetchall()
        
        # Get column names to map correctly
        cursor.execute("PRAGMA table_info(buku)")
        columns = [info[1] for info in cursor.fetchall()]
        
        for book in books:
            book_dict = dict(zip(columns, book))
            
            # Insert or find biblio
            cursor.execute('''
                SELECT id FROM bibliografi WHERE judul = ? AND (pengarang = ? OR pengarang IS NULL)
            ''', (book_dict.get('judul'), book_dict.get('pengarang')))
            biblio = cursor.fetchone()
            
            if not biblio:
                # Combine klasifikasi, cutter, huruf_judul into no_panggil
                no_panggil = f"{book_dict.get('klasifikasi', '')} {book_dict.get('cutter', '')} {book_dict.get('huruf_judul', '')}".strip()
                
                cursor.execute('''
                    INSERT INTO bibliografi (
                        judul, pengarang, edisi, gmd, isbn, penerbit, tahun_terbit, 
                        tempat_terbit, deskripsi_fisik, judul_seri, klasifikasi, no_panggil, 
                        subjek, bahasa, abstrak, gambar_sampul
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    book_dict.get('judul'), book_dict.get('pengarang'), book_dict.get('edisi'),
                    book_dict.get('gmd'), book_dict.get('isbn'), book_dict.get('penerbit'),
                    book_dict.get('tahun_terbit'), book_dict.get('tempat_terbit'),
                    book_dict.get('deskripsi_fisik'), book_dict.get('judul_seri'),
                    book_dict.get('klasifikasi'), no_panggil, book_dict.get('subjek'),
                    book_dict.get('bahasa'), book_dict.get('catatan'), book_dict.get('gambar_sampul')
                ))
                biblio_id = cursor.lastrowid
            else:
                biblio_id = biblio[0]
                
            # Insert eksemplar
            try:
                cursor.execute('''
                    INSERT INTO eksemplar (
                        no_induk, biblio_id, lokasi, status_buku, copy_ke, is_reference_only, tgl_terima
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    book_dict.get('no_induk'), biblio_id, book_dict.get('lokasi'),
                    book_dict.get('status_buku'), book_dict.get('copy_ke'),
                    book_dict.get('is_reference_only', 0), book_dict.get('tgl_terima')
                ))
            except sqlite3.IntegrityError:
                pass # Eksemplar already exists

    conn.commit()
    conn.close()
    print("Database restructured successfully to Relational SLiMS format.")

if __name__ == '__main__':
    migrate()
