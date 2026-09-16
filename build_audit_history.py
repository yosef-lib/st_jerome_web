import sqlite3
import codecs
import re

# 1. Create Table in Database
conn = sqlite3.connect('katalog.db')
conn.execute('''
CREATE TABLE IF NOT EXISTS audit_rak (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    no_induk TEXT NOT NULL,
    rak_target TEXT NOT NULL,
    status_audit TEXT NOT NULL,
    waktu_scan DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()
conn.close()

# 2. Update app.py
with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

# 2a. Update api_scan to insert data
old_audit_logic = '''        elif mode == 'audit_rak':
            klasifikasi = buku['klasifikasi']
            if not klasifikasi:
                return jsonify({
                    'status': 'warning',
                    'message': f'Buku "{buku["judul"]}" tidak memiliki DDC (Anomali Metadata).',
                    'buku': dict(buku)
                })
            
            ddc_awal = klasifikasi[0] + '00' # e.g. '2' -> '200'
            if ddc_awal == target_rak:
                return jsonify({
                    'status': 'success',
                    'message': f'BENAR: Buku "{buku["judul"]}" (DDC {klasifikasi}) berada di rak yang tepat.',
                    'buku': dict(buku)
                })
            else:
                return jsonify({
                    'status': 'danger',
                    'message': f'SALAH RAK! Buku "{buku["judul"]}" (DDC {klasifikasi}) seharusnya di Rak {ddc_awal}.',
                    'buku': dict(buku)
                })'''

new_audit_logic = '''        elif mode == 'audit_rak':
            klasifikasi = buku['klasifikasi']
            
            if not klasifikasi:
                status_audit = 'ANOMALI'
                msg = f'Buku "{buku["judul"]}" tidak memiliki DDC (Anomali Metadata).'
                json_status = 'warning'
            else:
                ddc_awal = klasifikasi[0] + '00'
                if ddc_awal == target_rak:
                    status_audit = 'BENAR'
                    msg = f'BENAR: Buku "{buku["judul"]}" (DDC {klasifikasi}) berada di rak yang tepat.'
                    json_status = 'success'
                else:
                    status_audit = 'SALAH RAK'
                    msg = f'SALAH RAK! Buku "{buku["judul"]}" (DDC {klasifikasi}) seharusnya di Rak {ddc_awal}.'
                    json_status = 'danger'

            # Simpan riwayat
            try:
                conn.execute('INSERT INTO audit_rak (no_induk, rak_target, status_audit) VALUES (?, ?, ?)', 
                            (no_induk, target_rak, status_audit))
            except Exception as e:
                print("Error saving audit:", e)
                
            return jsonify({
                'status': json_status,
                'message': msg,
                'buku': dict(buku)
            })'''

app_code = app_code.replace(old_audit_logic, new_audit_logic)

# 2b. Update /audit_rak route to fetch history and add /reset_audit
old_audit_route = '''@app.route('/audit_rak')
@login_required
def audit_rak():
    return render_template('audit_rak.html')'''

new_audit_route = '''@app.route('/audit_rak')
@login_required
def audit_rak():
    conn = database.get_db_connection()
    riwayat = conn.execute("""
        SELECT a.waktu_scan, a.rak_target, a.status_audit, b.no_induk, b.judul, b.klasifikasi
        FROM audit_rak a
        JOIN buku b ON a.no_induk = b.no_induk
        ORDER BY a.id DESC LIMIT 100
    """).fetchall()
    
    # Statistik
    stats = conn.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN status_audit = 'BENAR' THEN 1 ELSE 0 END) as benar,
            SUM(CASE WHEN status_audit = 'SALAH RAK' THEN 1 ELSE 0 END) as salah,
            SUM(CASE WHEN status_audit = 'ANOMALI' THEN 1 ELSE 0 END) as anomali
        FROM audit_rak
    """).fetchone()
    
    return render_template('audit_rak.html', riwayat=riwayat, stats=stats)

@app.route('/reset_audit', methods=['POST'])
@login_required
def reset_audit():
    conn = database.get_db_connection()
    conn.execute('DELETE FROM audit_rak')
    return redirect(url_for('audit_rak'))'''

app_code = app_code.replace(old_audit_route, new_audit_route)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)

print("audit logic updated")
