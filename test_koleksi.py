import codecs
with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

debug_api = '''
@app.route('/api/debug/koleksi', methods=['GET'])
def api_debug_koleksi():
    import traceback
    import database
    try:
        conn = database.get_db_connection()
        query = """
            SELECT b.*, COUNT(e.no_induk) as jumlah_eksemplar
            FROM bibliografi b
            LEFT JOIN eksemplar e ON b.id = e.biblio_id
            WHERE b.judul LIKE ?
            GROUP BY b.id
            ORDER BY b.id DESC
            LIMIT 10
        """
        cursor = conn.execute(query, ('%%',))
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify({'status': 'success', 'data': results})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e), 'trace': traceback.format_exc()})
'''

code += debug_api

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Debug koleksi API added")
