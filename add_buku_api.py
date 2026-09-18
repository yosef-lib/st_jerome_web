import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

new_api = '''
@app.route('/api/buku/<path:no_induk>', methods=['GET'])
@login_required
def get_buku(no_induk):
    conn = database.get_db_connection()
    buku = conn.execute("SELECT * FROM buku WHERE no_induk = ?", (no_induk,)).fetchone()
    conn.close()
    
    if buku:
        return jsonify({'status': 'success', 'data': dict(buku)})
    return jsonify({'status': 'error', 'message': 'Not found'}), 404
'''

anchor = "@app.route('/api/antrean', methods=['POST'])"
app_code = app_code.replace(anchor, new_api + '\n' + anchor)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)
print("api added")
