import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

# Fix: delete eksemplar by no_induk instead of id
old_delete_eks = '''@app.route('/api/eksemplar/<int:id>', methods=['DELETE'])
@login_required
def api_delete_eksemplar(id):
    import database
    conn = database.get_db_connection()
    conn.execute("DELETE FROM eksemplar WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})'''

new_delete_eks = '''@app.route('/api/eksemplar/<string:no_induk>', methods=['DELETE'])
@login_required
def api_delete_eksemplar(no_induk):
    import database
    conn = database.get_db_connection()
    conn.execute("DELETE FROM eksemplar WHERE no_induk = ?", (no_induk,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})'''

code = code.replace(old_delete_eks, new_delete_eks)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Fixed eksemplar delete")
