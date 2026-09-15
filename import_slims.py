import csv
import sqlite3
import database

def import_data():
    conn = database.get_db_connection()
    conn.execute('DELETE FROM buku')
    conn.execute('DELETE FROM buku_dibaca')
    
    # 1. Parse Biblio
    biblio_map = {}
    print("Reading biblio...")
    with open('senayan_biblio_export.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in reader:
            if len(row) < 18:
                continue
            item_code_raw = row[17]
            # Multiple item codes can be in one biblio row: <0001/21><0002/21>
            # Let's extract all item codes
            codes = [c.strip('<>') for c in item_code_raw.split('><')]
            for code in codes:
                code_clean = code.strip('<>')
                biblio_map[code_clean] = {
                    'title': row[0],
                    'gmd': row[1],
                    'edition': row[2],
                    'isbn': row[3],
                    'publisher': row[4],
                    'year': row[5],
                    'collation': row[6],
                    'call_number': row[8],
                    'language': row[9],
                    'place': row[10],
                    'classification': row[11],
                    'author': row[15].strip('<>').replace('><', ', '),
                    'subject': row[16].strip('<>').replace('><', ', ')
                }

    # 2. Parse Items and Insert
    print("Reading items and inserting...")
    inserted_count = 0
    with open('senayan_item_export.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in reader:
            if len(row) < 19:
                continue
                
            item_code = row[0]
            call_number = row[1]
            tgl_terima = row[4]
            lokasi_raw = row[7].upper()
            
            if 'IMAVI' in lokasi_raw:
                lokasi = 'IMAVI'
            else:
                lokasi = 'STPD'
                
            title = row[18]
            
            # Match biblio
            biblio = biblio_map.get(item_code, {})
            
            # Resolve fields
            final_title = biblio.get('title', title)
            gmd = biblio.get('gmd', '')
            edition = biblio.get('edition', '')
            isbn = biblio.get('isbn', '')
            publisher = biblio.get('publisher', '')
            year = biblio.get('year', '')
            collation = biblio.get('collation', '')
            language = biblio.get('language', '')
            place = biblio.get('place', '')
            classification = biblio.get('classification', '')
            author = biblio.get('author', '')
            subject = biblio.get('subject', '')
            
            # Cutter and huruf_judul heuristic from call_number
            # Format usually: Classification Cutter Huruf
            parts = call_number.split(' ')
            class_num = parts[0] if len(parts) > 0 else classification
            cutter = parts[1] if len(parts) > 1 else ''
            huruf = parts[2] if len(parts) > 2 else ''
            
            try:
                conn.execute('''
                    INSERT INTO buku (
                        no_induk, tgl_terima, status_buku, judul, pengarang, subjek, gmd, edisi, 
                        isbn, penerbit, tahun_terbit, tempat_terbit, deskripsi_fisik, 
                        bahasa, klasifikasi, cutter, huruf_judul, lokasi
                    ) VALUES (?, ?, 'SLIMS_IMPORT', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item_code, tgl_terima, final_title, author, subject, gmd, edition,
                    isbn, publisher, year, place, collation, language, class_num, cutter, huruf, lokasi
                ))
                inserted_count += 1
            except Exception as e:
                print(f"Error inserting {item_code}: {e}")
                
    conn.commit()
    conn.close()
    print(f"Successfully inserted {inserted_count} books.")

if __name__ == '__main__':
    import_data()
