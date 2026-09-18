import codecs
import re

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

api_code = '''
# ==============================================================
# API SIRKULASI (FASE 2)
# ==============================================================

@app.route('/api/sirkulasi/member/<member_id>', methods=['GET'])
@login_required
def api_get_member(member_id):
    conn = database.get_db_connection()
    member = conn.execute("SELECT * FROM anggota WHERE member_id = ?", (member_id,)).fetchone()
    if not member:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Anggota tidak ditemukan'})
        
    m = dict(member)
    
    # Hitung pinjaman aktif (buku yang belum dikembalikan)
    active_loans = conn.execute("SELECT COUNT(*) FROM sirkulasi WHERE member_id = ? AND return_date IS NULL", (member_id,)).fetchone()[0]
    
    # Hitung batas maksimal
    tipe = m.get('tipe_anggota', 'Reguler')
    if tipe is None:
        tipe = 'Reguler'
    max_loans = 4 if 'Skripsi' in tipe else 2
    
    # Cek suspend
    import datetime
    if m.get('status') == 'DIBLOKIR' and m.get('suspended_until'):
        suspend_date = datetime.datetime.strptime(m.get('suspended_until'), '%Y-%m-%d').date()
        today = datetime.datetime.now().date()
        if today >= suspend_date:
            conn.execute("UPDATE anggota SET status = ?, suspended_until = ? WHERE member_id = ?", ('AKTIF', None, member_id))
            conn.commit()
            m['status'] = 'AKTIF'
            m['suspended_until'] = None
    
    conn.close()
    return jsonify({
        'status': 'success',
        'data': {
            'id': m['member_id'],
            'nama': m['nama'],
            'tipe': tipe,
            'status': m['status'],
            'suspended_until': m.get('suspended_until', '-'),
            'active_loans': active_loans,
            'max_loans': max_loans
        }
    })

@app.route('/api/sirkulasi/borrow', methods=['POST'])
@login_required
def api_borrow():
    data = request.json
    member_id = data.get('member_id')
    book_id = data.get('book_id')
    
    conn = database.get_db_connection()
    eksemplar = conn.execute("SELECT e.*, b.judul FROM eksemplar e JOIN bibliografi b ON e.biblio_id = b.id WHERE e.no_induk = ?", (book_id,)).fetchone()
    
    if not eksemplar:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Buku dengan Barcode tersebut tidak ditemukan'})
        
    eksemplar = dict(eksemplar)
    if eksemplar.get('is_reference_only'):
        conn.close()
        return jsonify({'status': 'error', 'message': 'Buku ini adalah buku Referensi dan TIDAK BOLEH dipinjam.'})
    if eksemplar.get('status_buku') == 'DIPINJAM':
        conn.close()
        return jsonify({'status': 'error', 'message': 'Buku saat ini sedang berstatus dipinjam orang lain.'})
        
    import datetime
    loan_date = datetime.datetime.now()
    due_date = loan_date + datetime.timedelta(days=14)
    
    conn.execute("INSERT INTO sirkulasi (member_id, no_induk, loan_date, due_date) VALUES (?, ?, ?, ?)", (member_id, book_id, loan_date.strftime('%Y-%m-%d %H:%M:%S'), due_date.strftime('%Y-%m-%d %H:%M:%S')))
    conn.execute("UPDATE eksemplar SET status_buku = 'DIPINJAM' WHERE no_induk = ?", (book_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'data': {'buku_judul': eksemplar.get('judul')}})

def calculate_working_days(start_date, end_date, conn):
    import datetime
    libur_rows = conn.execute("SELECT tanggal FROM hari_libur").fetchall()
    libur_set = set(row[0] for row in libur_rows)
    
    days = (end_date - start_date).days
    working_days = 0
    for i in range(1, days + 1):
        day = start_date + datetime.timedelta(days=i)
        if day.weekday() < 5 and day.strftime('%Y-%m-%d') not in libur_set:
            working_days += 1
    return working_days

@app.route('/api/sirkulasi/return', methods=['POST'])
@login_required
def api_return():
    data = request.json
    book_id = data.get('book_id')
    
    conn = database.get_db_connection()
    loan = conn.execute("SELECT s.*, e.member_id as e_member_id, a.nama as anggota_nama, b.judul FROM sirkulasi s JOIN eksemplar e ON s.no_induk = e.no_induk JOIN bibliografi b ON e.biblio_id = b.id LEFT JOIN anggota a ON s.member_id = a.member_id WHERE s.no_induk = ? AND s.return_date IS NULL", (book_id,)).fetchone()
    
    if not loan:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Tidak ada catatan peminjaman aktif untuk buku ini.'})
        
    loan = dict(loan)
    import datetime
    
    return_datetime = datetime.datetime.now()
    due_datetime = datetime.datetime.strptime(loan['due_date'], '%Y-%m-%d %H:%M:%S')
    
    denda = 0
    terlambat_hari = 0
    
    if return_datetime.date() > due_datetime.date():
        terlambat_hari = calculate_working_days(due_datetime.date(), return_datetime.date(), conn)
        denda = terlambat_hari * 500
        
    conn.execute("UPDATE sirkulasi SET return_date = ?, fine_amount = ?, fine_status = ? WHERE id = ?", (return_datetime.strftime('%Y-%m-%d %H:%M:%S'), denda, 'BELUM_LUNAS' if denda > 0 else 'LUNAS', loan['id']))
    conn.execute("UPDATE eksemplar SET status_buku = 'TERSEDIA' WHERE no_induk = ?", (book_id,))
    
    if denda > 0:
        suspend_until = return_datetime.date() + datetime.timedelta(days=1)
        conn.execute("UPDATE anggota SET status = 'DIBLOKIR', suspended_until = ? WHERE member_id = ?", (suspend_until.strftime('%Y-%m-%d'), loan['member_id']))
        
    conn.commit()
    conn.close()
    
    return jsonify({
        'status': 'success',
        'data': {
            'buku_judul': loan.get('judul'),
            'anggota_nama': loan.get('anggota_nama'),
            'denda': denda,
            'terlambat_hari': terlambat_hari
        }
    })
'''

if "@app.route('/api/sirkulasi/member" not in code:
    code = code.replace("if __name__ == '__main__':", api_code + "\nif __name__ == '__main__':")
    with codecs.open('app.py', 'w', 'utf-8') as f:
        f.write(code)
    print("Added Sirkulasi APIs.")
else:
    print("APIs exist.")
