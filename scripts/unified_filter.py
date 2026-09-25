import codecs
import re

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

# I will replace the hardcoded date('now', 'localtime') and strftime('%Y-%m', 'now', 'localtime') 
# with a start_date and end_date.

old_def = '''@app.route('/analitik_kunjungan')
@login_required
def analitik_kunjungan():
    conn = database.get_db_connection()
    try:
        # Metrik 1: Kunjungan Hari Ini
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
        
        # Log Kunjungan Hari Ini
        log_hari_ini_rows = conn.execute("""
            SELECT waktu_kunjungan, identitas, tipe_pengunjung, asal_instansi, peran_jabatan, fakultas
            FROM sjla_visitor_logs
            WHERE date(waktu_kunjungan) = date('now', 'localtime')
            ORDER BY waktu_kunjungan DESC
        """).fetchall()
        log_hari_ini = [dict(row) for row in log_hari_ini_rows]
        
        # Metrik 3: Demografi Instansi (Bulan Ini)
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
            SELECT identitas, tipe_pengunjung, asal_instansi, peran_jabatan, fakultas, COUNT(id) as jumlah_kunjungan
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
                          member_hari_ini=member_hari_ini,
                          non_member_hari_ini=non_member_hari_ini,
                          fakultas_hari_ini=fakultas_hari_ini,
                          demografi=demografi, 
                          top_visitors=top_visitors,
                          log_hari_ini=log_hari_ini)'''

new_def = '''from datetime import datetime

@app.route('/analitik_kunjungan')
@login_required
def analitik_kunjungan():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Default: hari ini untuk rentang default jika tidak ada filter
    today_str = datetime.now().strftime('%Y-%m-%d')
    if not start_date:
        start_date = today_str
    if not end_date:
        end_date = today_str
        
    # Jika memfilter rentang bulan, kita bisa memilih tanggal awal bulan hingga akhir bulan.
    # Untuk query kita gunakan: date(waktu_kunjungan) >= start_date AND date(waktu_kunjungan) <= end_date
    
    conn = database.get_db_connection()
    try:
        # Metrik 1: Kunjungan (Filter)
        hari_ini_row = conn.execute("""
            SELECT 
                COUNT(id) as total,
                SUM(CASE WHEN tipe_pengunjung = 'Member' THEN 1 ELSE 0 END) as member_count,
                SUM(CASE WHEN tipe_pengunjung = 'Non-Member' THEN 1 ELSE 0 END) as non_member_count
            FROM sjla_visitor_logs 
            WHERE date(waktu_kunjungan) >= ? AND date(waktu_kunjungan) <= ?
        """, (start_date, end_date)).fetchone()
        kunjungan_hari_ini = hari_ini_row['total'] if hari_ini_row else 0
        member_hari_ini = hari_ini_row['member_count'] if hari_ini_row and hari_ini_row['member_count'] else 0
        non_member_hari_ini = hari_ini_row['non_member_count'] if hari_ini_row and hari_ini_row['non_member_count'] else 0
        
        # Metrik 2: Fakultas (Filter)
        fakultas_today_rows = conn.execute("""
            SELECT fakultas, COUNT(id) as jumlah
            FROM sjla_visitor_logs
            WHERE date(waktu_kunjungan) >= ? AND date(waktu_kunjungan) <= ? 
              AND fakultas IS NOT NULL AND fakultas != ''
            GROUP BY fakultas
            ORDER BY jumlah DESC
        """, (start_date, end_date)).fetchall()
        fakultas_hari_ini = [dict(row) for row in fakultas_today_rows]
        
        # Log Kunjungan (Filter)
        log_hari_ini_rows = conn.execute("""
            SELECT waktu_kunjungan, identitas, tipe_pengunjung, asal_instansi, peran_jabatan, fakultas
            FROM sjla_visitor_logs
            WHERE date(waktu_kunjungan) >= ? AND date(waktu_kunjungan) <= ?
            ORDER BY waktu_kunjungan DESC
        """, (start_date, end_date)).fetchall()
        log_hari_ini = [dict(row) for row in log_hari_ini_rows]
        
        # Metrik 3: Demografi Instansi (Filter)
        demografi_rows = conn.execute("""
            SELECT asal_instansi, COUNT(id) as jumlah 
            FROM sjla_visitor_logs 
            WHERE date(waktu_kunjungan) >= ? AND date(waktu_kunjungan) <= ?
            GROUP BY asal_instansi
            ORDER BY jumlah DESC
        """, (start_date, end_date)).fetchall()
        demografi = [dict(row) for row in demografi_rows]
        
        # Metrik 3: Top 10 Pengunjung (Filter)
        top_visitors = conn.execute("""
            SELECT identitas, tipe_pengunjung, asal_instansi, peran_jabatan, fakultas, COUNT(id) as jumlah_kunjungan
            FROM sjla_visitor_logs 
            WHERE date(waktu_kunjungan) >= ? AND date(waktu_kunjungan) <= ?
            GROUP BY identitas
            ORDER BY jumlah_kunjungan DESC
            LIMIT 10
        """, (start_date, end_date)).fetchall()
        
    finally:
        conn.close()
        
    return render_template('analitik_kunjungan.html', 
                          kunjungan_hari_ini=kunjungan_hari_ini, 
                          member_hari_ini=member_hari_ini,
                          non_member_hari_ini=non_member_hari_ini,
                          fakultas_hari_ini=fakultas_hari_ini,
                          demografi=demografi, 
                          top_visitors=top_visitors,
                          log_hari_ini=log_hari_ini,
                          start_date=start_date,
                          end_date=end_date)'''

app_code = app_code.replace(old_def, new_def)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)

print("Updated app.py unified filtering")
