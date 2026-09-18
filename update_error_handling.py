import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

code = code.replace('''
    # Get total for pagination
    total = conn.execute("SELECT COUNT(*) FROM bibliografi WHERE judul LIKE ? OR pengarang LIKE ?", (f'%{search}%', f'%{search}%')).fetchone()[0]
    
    conn.close()
    return jsonify({
''', '''
    # Get total for pagination
    total = conn.execute("SELECT COUNT(*) FROM bibliografi WHERE judul LIKE ? OR pengarang LIKE ?", (f'%{search}%', f'%{search}%')).fetchone()[0]
    
    conn.close()
    return jsonify({
''')

# Wait, let's wrap the whole api_koleksi_list in try except
import re

new_api = '''
@app.route('/api/koleksi/list', methods=['GET'])
@login_required
def api_koleksi_list():
    import traceback
    try:
        search = request.args.get('search', '')
        page = int(request.args.get('page', 1))
        per_page = 20
        offset = (page - 1) * per_page
        
        conn = database.get_db_connection()
        
        query = """
            SELECT b.*, COUNT(e.no_induk) as jumlah_eksemplar
            FROM bibliografi b
            LEFT JOIN eksemplar e ON b.id = e.biblio_id
            WHERE b.judul LIKE ? OR b.pengarang LIKE ? OR b.klasifikasi LIKE ?
            GROUP BY b.id
            ORDER BY b.id DESC
            LIMIT ? OFFSET ?
        """
        cursor = conn.execute(query, (f'%{search}%', f'%{search}%', f'%{search}%', per_page, offset))
        results = [dict(row) for row in cursor.fetchall()]
        
        total = conn.execute("SELECT COUNT(*) FROM bibliografi WHERE judul LIKE ? OR pengarang LIKE ?", (f'%{search}%', f'%{search}%')).fetchone()[0]
        conn.close()
        return jsonify({
            'data': results,
            'total': total,
            'page': page,
            'total_pages': (total // per_page) + (1 if total % per_page > 0 else 0)
        })
    except Exception as e:
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500
'''

code = re.sub(r"@app\.route\('/api/koleksi/list', methods=\['GET'\]\).*?total % per_page > 0 else 0\)\n    \}\)", new_api, code, flags=re.DOTALL)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Updated API")
