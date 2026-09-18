import codecs
import re

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

old_migration = '''        msg = "Tables created."
        cursor.execute("SELECT COUNT(*) FROM eksemplar")
        if cursor.fetchone()[0] == 0:
            cursor.execute("SELECT * FROM buku")
            buku_rows = cursor.fetchall()
            cursor.execute("PRAGMA table_info(buku)")
            columns = [col[1] for col in cursor.fetchall()]
            
            migrated_count = 0
            for row in buku_rows:
                row_dict = dict(zip(columns, row))
                cursor.execute("""
                    INSERT INTO bibliografi (
                        judul, gmd, edisi, isbn, penerbit, tahun_terbit, deskripsi_fisik, 
                        judul_seri, klasifikasi, cutter, huruf_judul, bahasa, tempat_terbit, 
                        pengarang, subjek
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row_dict.get('judul'), row_dict.get('gmd'), row_dict.get('edisi'), 
                    row_dict.get('isbn'), row_dict.get('penerbit'), row_dict.get('tahun_terbit'), 
                    row_dict.get('deskripsi_fisik'), row_dict.get('judul_seri'), 
                    row_dict.get('klasifikasi'), row_dict.get('cutter'), row_dict.get('huruf_judul'), 
                    row_dict.get('bahasa'), row_dict.get('tempat_terbit'), row_dict.get('pengarang'), 
                    row_dict.get('subjek')
                ))
                biblio_id = cursor.lastrowid
                
                cursor.execute("""
                    INSERT INTO eksemplar (
                        biblio_id, no_induk, status_buku, lokasi, tgl_terima, copy_ke, catatan
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    biblio_id, row_dict.get('no_induk'), row_dict.get('status_buku'), 
                    row_dict.get('lokasi'), row_dict.get('tgl_terima'), row_dict.get('copy_ke'), 
                    row_dict.get('catatan')
                ))
                migrated_count += 1
            msg += f" Migrated {migrated_count} records."'''

new_migration = '''        msg = "Tables created."
        # Selalu reset dan migrasi ulang untuk memperbaiki duplikat
        cursor.execute("DELETE FROM eksemplar")
        cursor.execute("DELETE FROM bibliografi")
        
        cursor.execute("SELECT * FROM buku")
        buku_rows = cursor.fetchall()
        cursor.execute("PRAGMA table_info(buku)")
        columns = [col[1] for col in cursor.fetchall()]
        
        biblio_map = {} # (judul, pengarang, penerbit) -> biblio_id
        
        migrated_count = 0
        for row in buku_rows:
            row_dict = dict(zip(columns, row))
            key = (row_dict.get('judul', ''), row_dict.get('pengarang', ''), row_dict.get('penerbit', ''))
            
            if key not in biblio_map:
                cursor.execute("""
                    INSERT INTO bibliografi (
                        judul, gmd, edisi, isbn, penerbit, tahun_terbit, deskripsi_fisik, 
                        judul_seri, klasifikasi, cutter, huruf_judul, bahasa, tempat_terbit, 
                        pengarang, subjek
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row_dict.get('judul'), row_dict.get('gmd'), row_dict.get('edisi'), 
                    row_dict.get('isbn'), row_dict.get('penerbit'), row_dict.get('tahun_terbit'), 
                    row_dict.get('deskripsi_fisik'), row_dict.get('judul_seri'), 
                    row_dict.get('klasifikasi'), row_dict.get('cutter'), row_dict.get('huruf_judul'), 
                    row_dict.get('bahasa'), row_dict.get('tempat_terbit'), row_dict.get('pengarang'), 
                    row_dict.get('subjek')
                ))
                biblio_map[key] = cursor.lastrowid
            
            biblio_id = biblio_map[key]
            
            cursor.execute("""
                INSERT INTO eksemplar (
                    biblio_id, no_induk, status_buku, lokasi, tgl_terima, copy_ke, catatan
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                biblio_id, row_dict.get('no_induk'), row_dict.get('status_buku'), 
                row_dict.get('lokasi'), row_dict.get('tgl_terima'), row_dict.get('copy_ke'), 
                row_dict.get('catatan')
            ))
            migrated_count += 1
        msg += f" Migrated {migrated_count} copies into {len(biblio_map)} titles."'''

code = code.replace(old_migration, new_migration)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Migration script updated to group titles.")
