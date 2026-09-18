import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

new_api = '''
@app.route('/api/sirkulasi/pay_fine', methods=['POST'])
@login_required
def api_pay_fine():
    data = request.json
    loan_id = data.get('loan_id')
    
    conn = database.get_db_connection()
    loan = conn.execute("SELECT * FROM sirkulasi WHERE id = ?", (loan_id,)).fetchone()
    
    if not loan:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Data peminjaman tidak ditemukan.'})
        
    conn.execute("UPDATE sirkulasi SET fine_status = 'LUNAS' WHERE id = ?", (loan_id,))
    
    # Check if user has any OTHER unpaid fines
    unpaid = conn.execute("SELECT COUNT(*) FROM sirkulasi WHERE member_id = ? AND fine_amount > 0 AND fine_status = 'BELUM_LUNAS'", (loan['member_id'],)).fetchone()[0]
    
    if unpaid == 0:
        # Unblock user
        conn.execute("UPDATE anggota SET status = 'AKTIF', suspended_until = NULL WHERE member_id = ?", (loan['member_id'],))
        
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'Denda lunas.'})
'''
# inject before api_borrow
code = code.replace("@app.route('/api/sirkulasi/borrow', methods=['POST'])", new_api + "\n@app.route('/api/sirkulasi/borrow', methods=['POST'])")

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("API pay_fine added.")
