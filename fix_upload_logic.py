import codecs
import re

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

old_logic = '''        df_biblio = pd.read_csv(biblio_path, dtype=str)
        df_item = pd.read_csv(item_path, dtype=str)
        
        # Merge logic
        if 'title' in df_biblio.columns and 'biblio_id' in df_item.columns:
            df = pd.merge(df_item, df_biblio, on='biblio_id', how='left')
        elif 'Judul' in df_biblio.columns and 'ID Bibliografi' in df_item.columns:
            df = pd.merge(df_item, df_biblio, left_on='ID Bibliografi', right_on='ID Bibliografi', how='left')
        else:
            bib_id_col = next((c for c in df_biblio.columns if 'id' in c.lower()), None)
            item_bib_id_col = next((c for c in df_item.columns if 'biblio' in c.lower() and 'id' in c.lower()), None)
            df = pd.merge(df_item, df_biblio, left_on=item_bib_id_col, right_on=bib_id_col, how='left')
            
        conn = database.get_db_connection()
        conn.execute('DELETE FROM buku')
        
        count = 0
        for _, row in df.iterrows():
            def get_val(cols):
                for c in cols:
                    if c in row and pd.notna(row[c]):
                        return str(row[c]).strip()
                return ''
                
            no_induk = get_val(['item_code', 'Kode Eksemplar', 'nomor_induk'])
            if not no_induk: continue
            
            judul = get_val(['title', 'Judul'])
            pengarang = get_val(['author', 'Pengarang'])
            lokasi = get_val(['location_name', 'Lokasi', 'lokasi'])
            klasifikasi = get_val(['classification', 'Klasifikasi'])
            subjek = get_val(['subject', 'Subjek'])
            
            gmd = get_val(['gmd_name', 'GMD'])
            edisi = get_val(['edition', 'Edisi'])
            isbn = get_val(['isbn_issn', 'ISBN/ISSN'])
            penerbit = get_val(['publisher_name', 'Penerbit'])
            tahun_terbit = get_val(['publish_year', 'Tahun Terbit'])
            tempat_terbit = get_val(['publish_place', 'Tempat Terbit'])
            deskripsi = get_val(['collation', 'Deskripsi Fisik'])
            status_buku = get_val(['item_status_name', 'Status'])
            tgl_terima = get_val(['received_date', 'Tanggal Terima'])
            
            # Use call_number from item if exists, otherwise fallback to parsing from classification
            # We will save call_number into classification, cutter, huruf_judul logic or directly if no_panggil existed.
            # But wait! Our DB schema doesn't have no_panggil! We fixed the SQL by concatenating klasifikasi, cutter, huruf_judul.
            # So we must parse the call_number back into klasifikasi, cutter, huruf_judul!
            call_number = get_val(['call_number', 'Nomor Panggil'])
            parts = call_number.split(' ') if call_number else []
            
            # If call number is present on item, override the biblio classification
            final_class = parts[0] if len(parts) > 0 else klasifikasi
            cutter = parts[1] if len(parts) > 1 else get_val(['classification_cutter', 'Cutter'])
            huruf = parts[2] if len(parts) > 2 else ''
            
            conn.execute("""
                INSERT INTO buku (no_induk, judul, pengarang, lokasi, klasifikasi, cutter, huruf_judul, subjek,
                                gmd, edisi, isbn, penerbit, tahun_terbit, tempat_terbit, 
                                deskripsi_fisik, status_buku, tgl_terima)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (no_induk, judul, pengarang, lokasi, final_class, cutter, huruf, subjek,
                  gmd, edisi, isbn, penerbit, tahun_terbit, tempat_terbit, 
                  deskripsi, status_buku, tgl_terima))
            count += 1
            
        conn.commit()
        conn.close()'''

new_logic = '''        import csv
        import re
        
        biblio_map = {}
        with open(biblio_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            headers = next(reader, None)
            for row in reader:
                if len(row) < 18: continue
                title = row[0]
                gmd = row[1]
                edisi = row[2]
                isbn = row[3]
                penerbit = row[4]
                tahun_terbit = row[5]
                deskripsi = row[6]
                klasifikasi = row[11]
                pengarang = row[15].strip('<>').replace('><', ', ')
                subjek = row[16].strip('<>').replace('><', ', ')
                
                item_code_raw = row[17]
                codes = re.findall(r'<(.*?)>', item_code_raw)
                if not codes and item_code_raw.strip():
                    codes = [item_code_raw.strip()]
                
                for code in codes:
                    biblio_map[code] = {
                        'title': title, 'gmd': gmd, 'edisi': edisi, 'isbn': isbn,
                        'penerbit': penerbit, 'tahun_terbit': tahun_terbit,
                        'deskripsi': deskripsi, 'klasifikasi': klasifikasi,
                        'pengarang': pengarang, 'subjek': subjek
                    }
                    
        conn = database.get_db_connection()
        conn.execute('DELETE FROM buku')
        
        count = 0
        with open(item_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            headers = next(reader, None)
            for row in reader:
                if len(row) < 10: continue
                no_induk = row[0]
                call_number = row[1]
                tgl_terima = row[4]
                lokasi_raw = row[7].upper()
                status_buku = row[9]
                
                lokasi = 'IMAVI' if 'IMAVI' in lokasi_raw else lokasi_raw
                
                bib = biblio_map.get(no_induk, {})
                judul = bib.get('title', row[18] if len(row) > 18 else '')
                pengarang = bib.get('pengarang', '')
                subjek = bib.get('subjek', '')
                gmd = bib.get('gmd', '')
                edisi = bib.get('edisi', '')
                isbn = bib.get('isbn', '')
                penerbit = bib.get('penerbit', '')
                tahun_terbit = bib.get('tahun_terbit', '')
                deskripsi = bib.get('deskripsi', '')
                klasifikasi = bib.get('klasifikasi', '')
                
                parts = call_number.split(' ') if call_number else []
                final_class = parts[0] if len(parts) > 0 else klasifikasi
                cutter = parts[1] if len(parts) > 1 else ''
                huruf = parts[2] if len(parts) > 2 else ''
                
                conn.execute("""
                    INSERT INTO buku (no_induk, judul, pengarang, lokasi, klasifikasi, cutter, huruf_judul, subjek,
                                    gmd, edisi, isbn, penerbit, tahun_terbit, tempat_terbit, 
                                    deskripsi_fisik, status_buku, tgl_terima)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (no_induk, judul, pengarang, lokasi, final_class, cutter, huruf, subjek,
                      gmd, edisi, isbn, penerbit, tahun_terbit, '', 
                      deskripsi, status_buku, tgl_terima))
                count += 1
                
        conn.commit()
        conn.close()'''

app_code = app_code.replace(old_logic, new_logic)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)

print("upload logic fixed")
