import codecs, re

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

old_post = '''@app.route('/api/antrean', methods=['POST'])
@login_required
def add_antrean():
    data = request.json
    
    # Save to SQLite DB
    conn = database.get_db_connection()
    try:
        conn.execute(\'''
            INSERT OR REPLACE INTO buku (
                no_induk, tgl_terima, status_buku, judul, pengarang, subjek, gmd, edisi, 
                isbn, penerbit, tahun_terbit, tempat_terbit, deskripsi_fisik, 
                judul_seri, bahasa, klasifikasi, cutter, huruf_judul, copy_ke, catatan, lokasi
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        \''', (
            data.get('no_induk'), data.get('tgl_terima'), data.get('status_buku'),
            data.get('judul'), data.get('pengarang'), data.get('subjek'),
            data.get('gmd'), data.get('edisi'), data.get('isbn'),
            data.get('penerbit'), data.get('tahun_terbit'), data.get('tempat_terbit'),
            data.get('deskripsi_fisik'), data.get('judul_seri'), data.get('bahasa'),
            data.get('klasifikasi'), data.get('cutter'), data.get('huruf_judul'),
            data.get('copy_ke'), data.get('catatan'), data.get('lokasi', 'STPD')
        ))
        conn.commit()
    except Exception as e:
        print("Error DB:", e)
    finally:
        conn.close()

    # Save to JSON Queue for printing
    queue = []
    if os.path.exists(ANTREAN_FILE):
        with open(ANTREAN_FILE, 'r') as f:
            try:
                queue = json.load(f)
            except:
                pass
                
    queue.append(data)
    with open(ANTREAN_FILE, 'w') as f:
        json.dump(queue, f)
        
    return jsonify({'status': 'success'})'''

new_post = '''@app.route('/api/antrean', methods=['POST'])
@login_required
def add_antrean():
    from werkzeug.utils import secure_filename
    if request.content_type and request.content_type.startswith('multipart/form-data'):
        data = request.form.to_dict()
        file = request.files.get('gambar_sampul')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            ext = os.path.splitext(filename)[1]
            safe_name = f"{data.get('no_induk', 'unknown').replace('/', '_')}{ext}"
            cover_dir = os.path.join(app.root_path, 'static', 'covers')
            os.makedirs(cover_dir, exist_ok=True)
            file.save(os.path.join(cover_dir, safe_name))
            data['gambar_sampul'] = safe_name
    else:
        data = request.json or {}
    
    # Save to SQLite DB
    conn = database.get_db_connection()
    try:
        conn.execute(\'''
            INSERT OR REPLACE INTO buku (
                no_induk, tgl_terima, status_buku, judul, pengarang, subjek, gmd, edisi, 
                isbn, penerbit, tahun_terbit, tempat_terbit, deskripsi_fisik, 
                judul_seri, bahasa, klasifikasi, cutter, huruf_judul, copy_ke, catatan, lokasi, gambar_sampul
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        \''', (
            data.get('no_induk'), data.get('tgl_terima'), data.get('status_buku'),
            data.get('judul'), data.get('pengarang'), data.get('subjek'),
            data.get('gmd'), data.get('edisi'), data.get('isbn'),
            data.get('penerbit'), data.get('tahun_terbit'), data.get('tempat_terbit'),
            data.get('deskripsi_fisik'), data.get('judul_seri'), data.get('bahasa'),
            data.get('klasifikasi'), data.get('cutter'), data.get('huruf_judul'),
            data.get('copy_ke'), data.get('catatan'), data.get('lokasi', 'STPD'),
            data.get('gambar_sampul')
        ))
        conn.commit()
    except Exception as e:
        print("Error DB:", e)
    finally:
        conn.close()

    # Save to JSON Queue for printing
    queue = []
    if os.path.exists(ANTREAN_FILE):
        with open(ANTREAN_FILE, 'r') as f:
            try:
                queue = json.load(f)
            except:
                pass
                
    queue.append(data)
    with open(ANTREAN_FILE, 'w') as f:
        json.dump(queue, f)
        
    return jsonify({'status': 'success'})'''

app_code = app_code.replace(old_post, new_post)
with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)
print("api/antrean POST updated")
