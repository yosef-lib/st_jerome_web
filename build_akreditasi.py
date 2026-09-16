import codecs
import re

with codecs.open('app.py', 'r', 'utf-8') as f:
    content = f.read()

# I will append the route at the end of the file, just before the if __name__ == '__main__':
new_route = '''
@app.route('/export_akreditasi')
@login_required
def export_akreditasi():
    lokasi = request.args.get('lokasi', 'STPD')
    conn = database.get_db_connection()
    
    # Gathering data
    akreditasi_judul_eks = conn.execute('SELECT COUNT(DISTINCT judul) as j, COUNT(no_induk) as e FROM buku WHERE lokasi = ?', (lokasi,)).fetchone()
    akreditasi_inti_umum = conn.execute("""
        SELECT 
            SUM(CASE WHEN SUBSTR(klasifikasi, 1, 1) IN ('1', '2') THEN 1 ELSE 0 END) as inti,
            SUM(CASE WHEN SUBSTR(klasifikasi, 1, 1) NOT IN ('1', '2') THEN 1 ELSE 0 END) as umum,
            COUNT(*) as total
        FROM buku WHERE lokasi = ?
    """, (lokasi,)).fetchone()
    
    # Create an excel file using pandas
    import pandas as pd
    from io import BytesIO
    from flask import send_file
    
    data = [
        {'Indikator': 'Jumlah Judul', 'Nilai': akreditasi_judul_eks['j']},
        {'Indikator': 'Jumlah Eksemplar', 'Nilai': akreditasi_judul_eks['e']},
        {'Indikator': 'Koleksi Inti (Teologi/Filsafat)', 'Nilai': akreditasi_inti_umum['inti']},
        {'Indikator': 'Koleksi Umum', 'Nilai': akreditasi_inti_umum['umum']},
        {'Indikator': 'Total Koleksi', 'Nilai': akreditasi_inti_umum['total']}
    ]
    
    df = pd.DataFrame(data)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Borang Akreditasi')
    
    output.seek(0)
    
    return send_file(
        output, 
        as_attachment=True, 
        download_name=f'Borang_Akreditasi_{lokasi}.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

if __name__ == '__main__':'''

content = content.replace("if __name__ == '__main__':", new_route)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(content)
print("akreditasi route added")
