import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

# 1. Update api_get_member to include history
old_member_fetch = '''    loans = [dict(row) for row in loans_cursor.fetchall()]

    conn.close()'''

new_member_fetch = '''    loans = [dict(row) for row in loans_cursor.fetchall()]

    # Fetch history loans (already returned)
    history_cursor = conn.execute("""
        SELECT s.*, e.no_induk, b.judul 
        FROM sirkulasi s
        JOIN eksemplar e ON s.no_induk = e.no_induk
        JOIN bibliografi b ON e.biblio_id = b.id
        WHERE s.member_id = ? AND s.return_date IS NOT NULL
        ORDER BY s.return_date DESC
    """, (member_id,))
    history_loans = [dict(row) for row in history_cursor.fetchall()]

    conn.close()'''

app_code = app_code.replace(old_member_fetch, new_member_fetch)

old_member_return = '''            'active_loans': active_loans,
            'max_loans': max_loans,
            'loans': loans
        }'''

new_member_return = '''            'active_loans': active_loans,
            'max_loans': max_loans,
            'loans': loans,
            'history_loans': history_loans
        }'''

app_code = app_code.replace(old_member_return, new_member_return)

# 2. Add /api/sirkulasi/renew endpoint
if "@app.route('/api/sirkulasi/renew'" not in app_code:
    renew_api = '''
@app.route('/api/sirkulasi/renew', methods=['POST'])
@login_required
def api_renew():
    data = request.json
    book_id = data.get('book_id')
    
    conn = database.get_db_connection()
    loan = conn.execute("""
        SELECT s.*, e.member_id as e_member_id, a.tipe_anggota 
        FROM sirkulasi s 
        JOIN eksemplar e ON s.no_induk = e.no_induk 
        LEFT JOIN anggota a ON s.member_id = a.member_id 
        WHERE s.no_induk = ? AND s.return_date IS NULL
    """, (book_id,)).fetchone()
    
    if not loan:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Tidak ada peminjaman aktif untuk buku ini.'})
        
    loan = dict(loan)
    tipe = loan.get('tipe_anggota', 'Reguler')
    if tipe is None:
        tipe = 'Reguler'
        
    # Check max renewals (Reguler = 2, Skripsi = unlimited)
    if 'Skripsi' not in tipe and loan['renewal_count'] >= 2:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Batas maksimal perpanjangan (2 kali) telah tercapai.'})
        
    import datetime
    # Perpanjang 14 hari dari HARI INI
    new_due_date = datetime.datetime.now() + datetime.timedelta(days=14)
    new_count = loan['renewal_count'] + 1
    
    conn.execute("UPDATE sirkulasi SET due_date = ?, renewal_count = ? WHERE id = ?", (new_due_date.strftime('%Y-%m-%d %H:%M:%S'), new_count, loan['id']))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'Berhasil diperpanjang 14 hari.', 'new_due_date': new_due_date.strftime('%Y-%m-%d')})
'''
    # Append before api_return to keep it grouped
    app_code = app_code.replace("@app.route('/api/sirkulasi/return'", renew_api + "\n@app.route('/api/sirkulasi/return'")

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)
print("Updated app.py with renew and history APIs")
