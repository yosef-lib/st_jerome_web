import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

# 1. Enhance autocomplete to return all fields
old_ac = '''@app.route('/api/kunjungan/autocomplete', methods=['GET'])
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
        conn.close()'''

new_ac = '''@app.route('/api/kunjungan/autocomplete', methods=['GET'])
def kunjungan_autocomplete():
    q = request.args.get('q', '').strip()
    if not q or len(q) < 3:
        return jsonify([])
        
    conn = database.get_db_connection()
    try:
        results = conn.execute("""
            SELECT identitas, asal_instansi, peran_jabatan, fakultas 
            FROM sjla_visitor_logs 
            WHERE tipe_pengunjung = 'Non-Member' AND identitas LIKE ?
            GROUP BY identitas
            LIMIT 10
        """, ('%' + q + '%',)).fetchall()
        
        suggestions = [dict(row) for row in results]
        return jsonify(suggestions)
    finally:
        conn.close()'''

app_code = app_code.replace(old_ac, new_ac)

# 2. Enhance analytics query to include Member vs Non-Member today, and Fakultas today
old_analitik = '''# Metrik 1: Kunjungan Hari Ini
        hari_ini_row = conn.execute("""
            SELECT COUNT(id) as total FROM sjla_visitor_logs 
            WHERE date(waktu_kunjungan) = date('now', 'localtime')
        """).fetchone()
        kunjungan_hari_ini = hari_ini_row['total'] if hari_ini_row else 0
        
        # Metrik 2: Demografi Instansi (Bulan Ini)
        demografi_rows = conn.execute("""
            SELECT asal_instansi, COUNT(id) as jumlah 
            FROM sjla_visitor_logs 
            WHERE strftime('%Y-%m', waktu_kunjungan) = strftime('%Y-%m', 'now', 'localtime')
            GROUP BY asal_instansi
            ORDER BY jumlah DESC
        """).fetchall()
        demografi = [dict(row) for row in demografi_rows]'''

new_analitik = '''# Metrik 1: Kunjungan Hari Ini
        hari_ini_row = conn.execute("""
            SELECT 
                COUNT(id) as total,
                SUM(CASE WHEN tipe_pengunjung = 'Member' THEN 1 ELSE 0 END) as member_count,
                SUM(CASE WHEN tipe_pengunjung = 'Non-Member' THEN 1 ELSE 0 END) as non_member_count
            FROM sjla_visitor_logs 
            WHERE date(waktu_kunjungan) = date('now', 'localtime')
        """).fetchone()
        kunjungan_hari_ini = hari_ini_row['total'] if hari_ini_row else 0
        member_hari_ini = hari_ini_row['member_count'] if hari_ini_row and hari_ini_row['member_count'] else 0
        non_member_hari_ini = hari_ini_row['non_member_count'] if hari_ini_row and hari_ini_row['non_member_count'] else 0
        
        # Metrik 2: Fakultas Hari Ini
        fakultas_today_rows = conn.execute("""
            SELECT fakultas, COUNT(id) as jumlah
            FROM sjla_visitor_logs
            WHERE date(waktu_kunjungan) = date('now', 'localtime') 
              AND fakultas IS NOT NULL AND fakultas != ''
            GROUP BY fakultas
            ORDER BY jumlah DESC
        """).fetchall()
        fakultas_hari_ini = [dict(row) for row in fakultas_today_rows]
        
        # Metrik 3: Demografi Instansi (Bulan Ini)
        demografi_rows = conn.execute("""
            SELECT asal_instansi, COUNT(id) as jumlah 
            FROM sjla_visitor_logs 
            WHERE strftime('%Y-%m', waktu_kunjungan) = strftime('%Y-%m', 'now', 'localtime')
            GROUP BY asal_instansi
            ORDER BY jumlah DESC
        """).fetchall()
        demografi = [dict(row) for row in demografi_rows]'''

app_code = app_code.replace(old_analitik, new_analitik)

# Update return render_template
old_render = '''return render_template('analitik_kunjungan.html', 
                          kunjungan_hari_ini=kunjungan_hari_ini, 
                          demografi=demografi, 
                          top_visitors=top_visitors)'''

new_render = '''return render_template('analitik_kunjungan.html', 
                          kunjungan_hari_ini=kunjungan_hari_ini, 
                          member_hari_ini=member_hari_ini,
                          non_member_hari_ini=non_member_hari_ini,
                          fakultas_hari_ini=fakultas_hari_ini,
                          demografi=demografi, 
                          top_visitors=top_visitors)'''
app_code = app_code.replace(old_render, new_render)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)

print("Updated app.py logic")
