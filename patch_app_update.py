import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

get_api = '''
@app.route('/api/bibliografi/get/<int:id>', methods=['GET'])
@login_required
def api_get_biblio(id):
    import database
    conn = database.get_db_connection()
    row = conn.execute("SELECT * FROM bibliografi WHERE id = ?", (id,)).fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    return jsonify({}), 404
'''
code += get_api

old_update = '''    elif image_filename:
        # Update existing bibliografi image if they upload a new one
        conn.execute("UPDATE bibliografi SET image = ? WHERE id = ?", (image_filename, biblio_id))'''

new_update = '''    else:
        # Update existing bibliografi
        update_query = """
            UPDATE bibliografi SET 
                judul=?, pengarang=?, penerbit=?, isbn=?, klasifikasi=?, tempat_terbit=?, 
                tahun_terbit=?, edisi=?, bahasa=?, gmd=?, deskripsi_fisik=?, judul_seri=?, 
                cutter=?, huruf_judul=?, subjek=?
            WHERE id=?
        """
        conn.execute(update_query, (
            data.get('judul'), data.get('pengarang'), data.get('penerbit'), data.get('isbn'),
            data.get('klasifikasi'), data.get('tempat_terbit'), data.get('tahun_terbit'),
            data.get('edisi'), data.get('bahasa', 'Indonesia'),
            data.get('gmd', 'Text'), data.get('deskripsi_fisik'), data.get('judul_seri'),
            data.get('cutter'), data.get('huruf_judul'), data.get('subjek'), biblio_id
        ))
        if image_filename:
            conn.execute("UPDATE bibliografi SET image = ? WHERE id = ?", (image_filename, biblio_id))'''

code = code.replace(old_update, new_update)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Patched app.py for update mode")
