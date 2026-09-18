import codecs
import re

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

new_api = '''def api_input_batch():
    from werkzeug.utils import secure_filename
    import os
    
    # Check if request is JSON (old behavior) or form data (new behavior with image)
    if request.is_json:
        data = request.json
    else:
        data = request.form

    biblio_id = data.get('biblio_id')
    jumlah_eksemplar = int(data.get('jumlah', 1))
    
    conn = database.get_db_connection()
    
    # Handle image upload
    image_filename = None
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            upload_dir = os.path.join(app.root_path, 'static', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            file.save(os.path.join(upload_dir, filename))
            image_filename = filename
    
    # 1. Handle Bibliografi
    if not biblio_id:
        # Create new bibliografi
        cursor = conn.execute("""
            INSERT INTO bibliografi (
                judul, pengarang, penerbit, isbn, klasifikasi, tempat_terbit, 
                tahun_terbit, edisi, bahasa, gmd, deskripsi_fisik, judul_seri, 
                cutter, huruf_judul, subjek, image
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get('judul'), data.get('pengarang'), data.get('penerbit'), data.get('isbn'),
            data.get('klasifikasi'), data.get('tempat_terbit'), data.get('tahun_terbit'),
            data.get('edisi'), data.get('bahasa', 'Indonesia'),
            data.get('gmd', 'Text'), data.get('deskripsi_fisik'), data.get('judul_seri'),
            data.get('cutter'), data.get('huruf_judul'), data.get('subjek'), image_filename
        ))
        biblio_id = cursor.lastrowid
    elif image_filename:
        # Update existing bibliografi image if they upload a new one
        conn.execute("UPDATE bibliografi SET image = ? WHERE id = ?", (image_filename, biblio_id))
'''

code = re.sub(r'def api_input_batch\(\):\n    data = request\.json.*?biblio_id = cursor\.lastrowid', new_api, code, flags=re.DOTALL)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Patched app.py for image upload")
