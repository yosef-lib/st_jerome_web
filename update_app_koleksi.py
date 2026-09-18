import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

# Replace the old /koleksi and /api/buku endpoints
import re
code = re.sub(r"@app\.route\('/koleksi'\).*?return render_template\('koleksi\.html'\)", "@app.route('/koleksi')\n@login_required\ndef koleksi():\n    return render_template('koleksi.html')", code, flags=re.DOTALL)

new_koleksi_api = '''
@app.route('/api/koleksi/list', methods=['GET'])
@login_required
def api_koleksi_list():
    search = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    per_page = 20
    offset = (page - 1) * per_page
    
    conn = database.get_db_connection()
    
    query = """
        SELECT b.*, COUNT(e.id) as jumlah_eksemplar
        FROM bibliografi b
        LEFT JOIN eksemplar e ON b.id = e.biblio_id
        WHERE b.judul LIKE ? OR b.pengarang LIKE ? OR b.klasifikasi LIKE ?
        GROUP BY b.id
        ORDER BY b.id DESC
        LIMIT ? OFFSET ?
    """
    cursor = conn.execute(query, (f'%{search}%', f'%{search}%', f'%{search}%', per_page, offset))
    results = [dict(row) for row in cursor.fetchall()]
    
    # Get total for pagination
    total = conn.execute("SELECT COUNT(*) FROM bibliografi WHERE judul LIKE ? OR pengarang LIKE ?", (f'%{search}%', f'%{search}%')).fetchone()[0]
    
    conn.close()
    return jsonify({
        'data': results,
        'total': total,
        'page': page,
        'total_pages': (total // per_page) + (1 if total % per_page > 0 else 0)
    })

@app.route('/api/koleksi/eksemplar/<int:biblio_id>', methods=['GET'])
@login_required
def api_koleksi_eksemplar(biblio_id):
    conn = database.get_db_connection()
    cursor = conn.execute("SELECT no_induk, status_ketersediaan, status_buku, lokasi, tgl_terima FROM eksemplar WHERE biblio_id = ? ORDER BY no_induk", (biblio_id,))
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)
'''
code += new_koleksi_api

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Koleksi APIs added.")
