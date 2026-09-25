import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

# Update the POST API logic to include peran_jabatan
old_api = '''@app.route('/api/kunjungan', methods=['POST'])
def submit_kunjungan():
    data = request.json
    tipe_pengunjung = data.get('tipe_pengunjung', 'Non-Member')
    identitas = data.get('identitas', '').strip()
    asal_instansi = data.get('asal_instansi', '').strip()
    tujuan = data.get('tujuan_kunjungan', '').strip()
    
    if not identitas:
        return jsonify({"status": "error", "message": "Identitas tidak boleh kosong!"}), 400
        
    conn = database.get_db_connection()
    try:
        # Pastikan tabel exist (safeguard)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS sjla_visitor_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            waktu_kunjungan DATETIME DEFAULT (datetime('now', 'localtime')),
            tipe_pengunjung TEXT,
            identitas TEXT,
            asal_instansi TEXT,
            tujuan_kunjungan TEXT
        )
        """)
        
        member_name = None
        if tipe_pengunjung == 'Member':
            # Verifikasi ID di tabel anggota
            member = conn.execute("SELECT member_name, instansi FROM anggota WHERE member_id = ?", (identitas,)).fetchone()
            if member:
                member_name = member['member_name']
                asal_instansi = member['instansi'] or 'Internal'
            else:
                return jsonify({"status": "error", "message": f"Member dengan ID {identitas} tidak ditemukan."}), 404
        
        # Simpan log
        conn.execute("""
            INSERT INTO sjla_visitor_logs (tipe_pengunjung, identitas, asal_instansi, tujuan_kunjungan)
            VALUES (?, ?, ?, ?)
        """, (tipe_pengunjung, identitas, asal_instansi, tujuan))
        conn.commit()'''

new_api = '''@app.route('/api/kunjungan', methods=['POST'])
def submit_kunjungan():
    data = request.json
    tipe_pengunjung = data.get('tipe_pengunjung', 'Non-Member')
    identitas = data.get('identitas', '').strip()
    asal_instansi = data.get('asal_instansi', '').strip()
    peran = data.get('peran_jabatan', '').strip()
    
    if not identitas:
        return jsonify({"status": "error", "message": "Identitas tidak boleh kosong!"}), 400
        
    conn = database.get_db_connection()
    try:
        # Safeguard if column doesn't exist for some reason
        try:
            conn.execute("ALTER TABLE sjla_visitor_logs ADD COLUMN peran_jabatan TEXT")
        except:
            pass
            
        member_name = None
        if tipe_pengunjung == 'Member':
            # Verifikasi ID di tabel anggota
            member = conn.execute("SELECT member_name, instansi FROM anggota WHERE member_id = ?", (identitas,)).fetchone()
            if member:
                member_name = member['member_name']
                asal_instansi = member['instansi'] or 'Internal'
            else:
                return jsonify({"status": "error", "message": f"Member dengan ID {identitas} tidak ditemukan."}), 404
        
        # Simpan log
        conn.execute("""
            INSERT INTO sjla_visitor_logs (tipe_pengunjung, identitas, asal_instansi, peran_jabatan)
            VALUES (?, ?, ?, ?)
        """, (tipe_pengunjung, identitas, asal_instansi, peran))
        conn.commit()'''

app_code = app_code.replace(old_api, new_api)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)

print("API updated")
