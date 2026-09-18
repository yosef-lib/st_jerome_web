import codecs
import re

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

new_api = '''import os
from werkzeug.utils import secure_filename

@app.route('/api/bibliografi', methods=['POST'])
@login_required
def api_bibliografi():
    conn = database.get_db_connection()
    try:
        # Handle file upload
        gambar_filename = None
        if 'gambar_sampul' in request.files:
            file = request.files['gambar_sampul']
            if file and file.filename != '':
                upload_folder = os.path.join('static', 'uploads', 'covers')
                os.makedirs(upload_folder, exist_ok=True)
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_folder, filename))
                gambar_filename = filename

        # Insert Bibliografi
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO bibliografi (
                judul, pengarang, pernyataan_tanggungjawab, edisi, info_detail_spesifik,
                gmd, tipe_isi, tipe_media, tipe_pembawa, kala_terbit, isbn, penerbit,
                tahun_terbit, tempat_terbit, deskripsi_fisik, judul_seri, klasifikasi,
                no_panggil, subjek, bahasa, abstrak, gambar_sampul
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            request.form.get('judul'), request.form.get('pengarang'), request.form.get('pernyataan_tanggungjawab'),
            request.form.get('edisi'), request.form.get('info_detail_spesifik'), request.form.get('gmd'),
            request.form.get('tipe_isi'), request.form.get('tipe_media'), request.form.get('tipe_pembawa'),
            request.form.get('kala_terbit'), request.form.get('isbn'), request.form.get('penerbit'),
            request.form.get('tahun_terbit'), request.form.get('tempat_terbit'), request.form.get('deskripsi_fisik'),
            request.form.get('judul_seri'), request.form.get('klasifikasi'), request.form.get('no_panggil'),
            request.form.get('subjek'), request.form.get('bahasa', 'Indonesia'), request.form.get('abstrak'),
            gambar_filename
        ))
        biblio_id = cursor.lastrowid
        
        # Insert Eksemplar
        pola = request.form.get('pola_eksemplar')
        lokasi = request.form.get('lokasi', 'IMAVI')
        is_ref = 1 if request.form.get('is_reference_only') else 0
        eksemplar_count = 0
        
        if not pola:
            # Manual single barcode
            barcode = request.form.get('manual_barcode')
            if barcode:
                cursor.execute("""
                    INSERT INTO eksemplar (no_induk, biblio_id, lokasi, is_reference_only, copy_ke)
                    VALUES (?, ?, ?, ?, 1)
                """, (barcode, biblio_id, lokasi, is_ref))
                eksemplar_count = 1
        else:
            # Pattern generation (e.g. B00000 -> B00001, B00002)
            prefix = re.sub(r'0+$', '', pola)
            pad_len = len(pola) - len(prefix)
            total = int(request.form.get('total_item', 1))
            
            # Find max current for this prefix
            cursor.execute("SELECT no_induk FROM eksemplar WHERE no_induk LIKE ? ORDER BY no_induk DESC LIMIT 1", (prefix + '%',))
            last_item = cursor.fetchone()
            start_num = 1
            if last_item:
                import re as regex
                match = regex.search(r'\d+$', last_item[0])
                if match:
                    start_num = int(match.group()) + 1
            
            for i in range(total):
                num_str = str(start_num + i).zfill(pad_len)
                barcode = f"{prefix}{num_str}"
                cursor.execute("""
                    INSERT INTO eksemplar (no_induk, biblio_id, lokasi, is_reference_only, copy_ke)
                    VALUES (?, ?, ?, ?, ?)
                """, (barcode, biblio_id, lokasi, is_ref, i+1))
            eksemplar_count = total
            
        conn.commit()
        return jsonify({'status': 'success', 'eksemplar_count': eksemplar_count})
        
    except sqlite3.IntegrityError as e:
        return jsonify({'status': 'error', 'message': 'Barcode duplikat / No Induk sudah dipakai.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    finally:
        conn.close()

# Keep API Buku for backward compatibility if needed, or we just put this above api_buku
'''

code = code.replace("@app.route('/api/buku'", new_api + "\n@app.route('/api/buku'")

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Updated app.py with api_bibliografi")
