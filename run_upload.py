import pandas as pd
import sqlite3

def run_import():
    try:
        df_biblio = pd.read_csv('senayan_biblio_export.csv', dtype=str)
        df_item = pd.read_csv('senayan_item_export.csv', dtype=str)
        
        # Merge
        if 'title' in df_biblio.columns and 'biblio_id' in df_item.columns:
            df = pd.merge(df_item, df_biblio, on='biblio_id', how='left')
        elif 'Judul' in df_biblio.columns and 'ID Bibliografi' in df_item.columns:
            # Maybe Indonesian columns
            df = pd.merge(df_item, df_biblio, left_on='ID Bibliografi', right_on='ID Bibliografi', how='left')
        else:
            # Try to guess
            bib_id_col = next((c for c in df_biblio.columns if 'id' in c.lower()), None)
            item_bib_id_col = next((c for c in df_item.columns if 'biblio' in c.lower() and 'id' in c.lower()), None)
            df = pd.merge(df_item, df_biblio, left_on=item_bib_id_col, right_on=bib_id_col, how='left')
            
        print(f"Merged dataframe has {len(df)} rows")
        
        # Clear existing
        conn = sqlite3.connect('katalog.db')
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
            
            # Map other fields
            gmd = get_val(['gmd_name', 'GMD'])
            edisi = get_val(['edition', 'Edisi'])
            isbn = get_val(['isbn_issn', 'ISBN/ISSN'])
            penerbit = get_val(['publisher_name', 'Penerbit'])
            tahun_terbit = get_val(['publish_year', 'Tahun Terbit'])
            tempat_terbit = get_val(['publish_place', 'Tempat Terbit'])
            deskripsi = get_val(['collation', 'Deskripsi Fisik'])
            status_buku = get_val(['item_status_name', 'Status'])
            tgl_terima = get_val(['received_date', 'Tanggal Terima'])
            cutter = get_val(['classification_cutter', 'Cutter'])
            
            # The uploaded file might not have cutter, wait, let's just grab everything we can.
            conn.execute('''
                INSERT INTO buku (no_induk, judul, pengarang, lokasi, klasifikasi, subjek,
                                gmd, edisi, isbn, penerbit, tahun_terbit, tempat_terbit, 
                                deskripsi_fisik, status_buku, tgl_terima)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (no_induk, judul, pengarang, lokasi, klasifikasi, subjek,
                  gmd, edisi, isbn, penerbit, tahun_terbit, tempat_terbit, 
                  deskripsi, status_buku, tgl_terima))
            count += 1
            
        conn.commit()
        conn.close()
        print(f"Successfully inserted {count} books!")
        
    except Exception as e:
        print("Error:", e)
        
run_import()
