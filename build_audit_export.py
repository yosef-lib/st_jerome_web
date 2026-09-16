import codecs
import re

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

# Replace reset_audit with export_audit
old_reset = '''@app.route('/reset_audit', methods=['POST'])
@login_required
def reset_audit():
    conn = database.get_db_connection()
    conn.execute('DELETE FROM audit_rak')
    return redirect(url_for('audit_rak'))'''

new_export = '''@app.route('/export_audit')
@login_required
def export_audit():
    import pandas as pd
    from io import BytesIO
    from flask import send_file
    
    conn = database.get_db_connection()
    df = pd.read_sql_query("""
        SELECT a.waktu_scan as 'Waktu Scan', a.no_induk as 'No Induk', b.judul as 'Judul Buku', a.rak_target as 'Target Rak', a.status_audit as 'Status', b.klasifikasi as 'DDC Seharusnya'
        FROM audit_rak a
        JOIN buku b ON a.no_induk = b.no_induk
        ORDER BY a.id DESC
    """, conn)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Riwayat Audit')
    
    output.seek(0)
    
    return send_file(
        output, 
        as_attachment=True, 
        download_name='Laporan_Audit_Rak.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )'''

app_code = app_code.replace(old_reset, new_export)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)

print("app updated")

# Update audit_rak.html
with codecs.open('templates/audit_rak.html', 'r', 'utf-8') as f:
    html = f.read()

old_btn = '''                <form action="/reset_audit" method="POST" onsubmit="return confirm('Yakin ingin menghapus seluruh riwayat stok opname saat ini? Pastikan Anda sudah merekapnya.');">
                    <button type="submit" class="flex items-center gap-2 rounded bg-danger py-2 px-4 font-medium text-white hover:bg-opacity-90 transition text-sm">
                        <i class="fa-solid fa-trash"></i> Reset Data
                    </button>
                </form>'''

new_btn = '''                <a href="/export_audit" class="flex items-center gap-2 rounded bg-success py-2 px-4 font-medium text-white hover:bg-opacity-90 transition text-sm">
                    <i class="fa-solid fa-file-excel"></i> Ekspor ke Excel
                </a>'''

html = html.replace(old_btn, new_btn)

with codecs.open('templates/audit_rak.html', 'w', 'utf-8') as f:
    f.write(html)
    
print("html updated")
