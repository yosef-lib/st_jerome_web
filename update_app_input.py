import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

new_apis = '''
@app.route('/api/ddc/search', methods=['GET'])
@login_required
def api_ddc_search():
    keyword = request.args.get('q', '').lower()
    import json
    import os
    try:
        with open('ddc_kamus.json', 'r') as f:
            ddc_dict = json.load(f)
    except:
        ddc_dict = {}
        
    results = []
    for code, desc in ddc_dict.items():
        if keyword in desc.lower():
            results.append({'kode': code, 'deskripsi': desc})
    return jsonify(results)

@app.route('/api/bibliografi/search', methods=['GET'])
@login_required
def api_biblio_search():
    keyword = request.args.get('q', '')
    conn = database.get_db_connection()
    # Search by title or author
    cursor = conn.execute("SELECT * FROM bibliografi WHERE judul LIKE ? OR pengarang LIKE ? LIMIT 10", (f'%{keyword}%', f'%{keyword}%'))
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

@app.route('/api/buku/input_batch', methods=['POST'])
@login_required
def api_input_batch():
    data = request.json
    biblio_id = data.get('biblio_id')
    jumlah_eksemplar = int(data.get('jumlah', 1))
    
    conn = database.get_db_connection()
    
    # 1. Handle Bibliografi
    if not biblio_id:
        # Create new bibliografi
        cursor = conn.execute("""
            INSERT INTO bibliografi (judul, pengarang, penerbit, isbn, klasifikasi, tempat_terbit, tahun_terbit, edisi, bahasa)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get('judul'), data.get('pengarang'), data.get('penerbit'), data.get('isbn'),
            data.get('klasifikasi'), data.get('tempat_terbit'), data.get('tahun_terbit'),
            data.get('edisi'), data.get('bahasa', 'Indonesia')
        ))
        biblio_id = cursor.lastrowid
    
    # 2. Generate Barcodes (No Induk)
    import datetime
    current_year = datetime.datetime.now().strftime('%y') # e.g. '26'
    
    # Find max sequence for this year in eksemplar
    max_seq_row = conn.execute("SELECT no_induk FROM eksemplar WHERE no_induk LIKE ? ORDER BY no_induk DESC LIMIT 1", (f'%/{current_year}',)).fetchone()
    
    start_num = 1
    if max_seq_row:
        try:
            start_num = int(max_seq_row[0].split('/')[0]) + 1
        except:
            start_num = 1
            
    generated_barcodes = []
    for i in range(jumlah_eksemplar):
        new_barcode = f"{(start_num + i):04d}/{current_year}"
        conn.execute("""
            INSERT INTO eksemplar (biblio_id, no_induk, status_buku, lokasi, tgl_terima, copy_ke)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            biblio_id, new_barcode, data.get('status_buku', 'BELI'), data.get('lokasi', 'IMAVI'),
            datetime.datetime.now().strftime('%Y-%m-%d'), (i+1)
        ))
        generated_barcodes.append(new_barcode)
        
    conn.commit()
    conn.close()
    
    return jsonify({
        'status': 'success', 
        'message': f'Berhasil menyimpan bibliografi dan {jumlah_eksemplar} eksemplar.',
        'barcodes': generated_barcodes
    })
'''

# Find the end of app.py and append
code += new_apis

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Input batch APIs added.")
