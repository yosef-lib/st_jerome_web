import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

new_routes = '''

# ==========================================
# BUKU TAMU PENGUNJUNG (KIOSK)
# ==========================================

@app.route('/kiosk')
def kiosk():
    # Halaman Kiosk bersifat publik (tanpa login_required) untuk ditaruh di lobi
    return render_template('kiosk.html')

@app.route('/api/kunjungan/autocomplete', methods=['GET'])
def kunjungan_autocomplete():
    q = request.args.get('q', '').strip()
    if not q or len(q) < 3:
        return jsonify([])
        
    conn = database.get_db_connection()
    try:
        # Cari nama tamu yang mirip dari riwayat kunjungan (case-insensitive)
        results = conn.execute("""
            SELECT DISTINCT identitas FROM sjla_visitor_logs 
            WHERE tipe_pengunjung = 'Non-Member' AND identitas LIKE ?
            LIMIT 10
        """, ('%' + q + '%',)).fetchall()
        
        suggestions = [row['identitas'] for row in results]
        return jsonify(suggestions)
    finally:
        conn.close()

@app.route('/api/kunjungan', methods=['POST'])
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
        conn.commit()
        
        display_name = member_name if member_name else identitas
        return jsonify({
            "status": "success", 
            "message": f"Selamat datang, {display_name}!",
            "display_name": display_name
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

'''

if "def kiosk():" not in app_code:
    app_code = app_code.replace("if __name__ == '__main__':", new_routes + "\nif __name__ == '__main__':")
    with codecs.open('app.py', 'w', 'utf-8') as f:
        f.write(app_code)
    print("Routes injected.")
else:
    print("Routes already exist.")
