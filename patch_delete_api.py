import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

delete_apis = '''
@app.route('/api/bibliografi/<int:id>', methods=['DELETE'])
@login_required
def api_delete_biblio(id):
    import database
    conn = database.get_db_connection()
    # Delete eksemplar first
    conn.execute("DELETE FROM eksemplar WHERE biblio_id = ?", (id,))
    # Delete bibliografi
    conn.execute("DELETE FROM bibliografi WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/api/eksemplar/<int:id>', methods=['DELETE'])
@login_required
def api_delete_eksemplar(id):
    import database
    conn = database.get_db_connection()
    conn.execute("DELETE FROM eksemplar WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})
'''

code += delete_apis

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Added DELETE APIs")
