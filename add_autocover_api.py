import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

new_routes = """
@app.route('/api/buku/missing_covers', methods=['GET'])
def api_missing_covers():
    conn = database.get_db_connection()
    # Get up to 100 books that lack both ISBN and image
    cursor = conn.execute("SELECT id, judul, pengarang FROM bibliografi WHERE (isbn IS NULL OR isbn = '') AND (image IS NULL OR image = '') LIMIT 100")
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

@app.route('/api/buku/save_cover', methods=['POST'])
def api_save_cover():
    data = request.json
    biblio_id = data.get('id')
    url = data.get('url')
    if biblio_id and url:
        conn = database.get_db_connection()
        conn.execute("UPDATE bibliografi SET image = ? WHERE id = ?", (url, biblio_id))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'})
"""

# Insert before if __name__ == '__main__':
code = code.replace("if __name__ == '__main__':", new_routes + "\nif __name__ == '__main__':")

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Added missing_covers routes")
