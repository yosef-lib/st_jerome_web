import codecs

new_route = '''
import pandas as pd
import os
from werkzeug.utils import secure_filename

@app.route('/import_slims', methods=['GET', 'POST'])
@login_required
def import_slims():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part", 400
        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400
            
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join('static', filename)
            file.save(filepath)
            
            try:
                df = pd.read_excel(filepath)
                conn = database.get_db_connection()
                
                # Buat tabel jika belum ada
                conn.execute("""
                CREATE TABLE IF NOT EXISTS peminjaman (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    member_id TEXT,
                    member_name TEXT,
                    no_induk TEXT,
                    judul TEXT,
                    loan_date TEXT,
                    due_date TEXT,
                    loan_status TEXT
                )
                """)
                # Hapus data lama agar terganti yang baru
                conn.execute('DELETE FROM peminjaman')
                
                for index, row in df.iterrows():
                    no_induk = str(row.get('Item Code', ''))
                    if no_induk == 'nan' or pd.isna(row.get('Item Code')): no_induk = ''
                    
                    loan_date = str(row.get('Loan Date', ''))
                    if loan_date == 'nan' or pd.isna(row.get('Loan Date')): loan_date = ''
                    
                    conn.execute("""
                        INSERT INTO peminjaman (member_id, member_name, no_induk, judul, loan_date, due_date, loan_status)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        str(row.get('Member ID', '')),
                        str(row.get('Member Name', '')),
                        no_induk,
                        str(row.get('Title', '')),
                        loan_date,
                        str(row.get('Due Date', '')),
                        str(row.get('Loan Status', ''))
                    ))
                conn.commit()
                conn.close()
                os.remove(filepath)
                return "<script>alert('Sukses sinkronisasi data SLiMS!'); window.location.href='/analisis_lanjutan?lokasi=IMAVI';</script>"
            except Exception as e:
                return f"Error memproses file: {str(e)}", 500
                
    return render_template('import_slims.html')
'''

with codecs.open('app.py', 'r', 'utf-8') as f:
    content = f.read()

content = content.replace("if __name__ == '__main__':", new_route + "\nif __name__ == '__main__':")

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(content)
print("Upload route added")
