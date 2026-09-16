import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

analytics_routes = '''

# ==========================================
# ANALITIK KUNJUNGAN (FASE 2)
# ==========================================

@app.route('/analitik_kunjungan')
@login_required
def analitik_kunjungan():
    conn = database.get_db_connection()
    try:
        # Metrik 1: Kunjungan Hari Ini
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
        demografi = [dict(row) for row in demografi_rows]
        
        # Metrik 3: Top 10 Pengunjung (Bulan Ini)
        top_visitors = conn.execute("""
            SELECT identitas, tipe_pengunjung, asal_instansi, peran_jabatan, COUNT(id) as jumlah_kunjungan
            FROM sjla_visitor_logs 
            WHERE strftime('%Y-%m', waktu_kunjungan) = strftime('%Y-%m', 'now', 'localtime')
            GROUP BY identitas
            ORDER BY jumlah_kunjungan DESC
            LIMIT 10
        """).fetchall()
        
    finally:
        conn.close()
        
    return render_template('analitik_kunjungan.html', 
                          kunjungan_hari_ini=kunjungan_hari_ini, 
                          demografi=demografi, 
                          top_visitors=top_visitors)

@app.route('/export_kunjungan', methods=['POST'])
@login_required
def export_kunjungan():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    
    if not start_date or not end_date:
        flash('Pilih rentang tanggal terlebih dahulu.', 'danger')
        return redirect(url_for('analitik_kunjungan'))
        
    conn = database.get_db_connection()
    query = """
        SELECT 
            waktu_kunjungan as 'Waktu Kunjungan',
            identitas as 'Nama/ID Pengunjung',
            tipe_pengunjung as 'Status Member',
            asal_instansi as 'Instansi',
            peran_jabatan as 'Peran/Jabatan',
            fakultas as 'Fakultas'
        FROM sjla_visitor_logs
        WHERE date(waktu_kunjungan) >= ? AND date(waktu_kunjungan) <= ?
        ORDER BY waktu_kunjungan DESC
    """
    df = pd.read_sql_query(query, conn, params=(start_date, end_date))
    conn.close()
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Laporan Kunjungan')
    
    output.seek(0)
    
    return send_file(
        output, 
        as_attachment=True, 
        download_name=f'Laporan_Kunjungan_{start_date}_sd_{end_date}.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

'''

if "def analitik_kunjungan():" not in app_code:
    app_code = app_code.replace("if __name__ == '__main__':", analytics_routes + "\nif __name__ == '__main__':")
    with codecs.open('app.py', 'w', 'utf-8') as f:
        f.write(app_code)
    print("Analytics routes injected.")
else:
    print("Analytics routes already exist.")
