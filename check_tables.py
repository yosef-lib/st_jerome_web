import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

debug_api = '''
@app.route('/api/debug/tables', methods=['GET'])
def api_debug_tables():
    import database
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    eksemplar_count = 0
    sirkulasi_count = 0
    if 'eksemplar' in tables:
        eksemplar_count = conn.execute("SELECT COUNT(*) FROM eksemplar").fetchone()[0]
    if 'sirkulasi' in tables:
        sirkulasi_count = conn.execute("SELECT COUNT(*) FROM sirkulasi").fetchone()[0]
        
    conn.close()
    return jsonify({
        'tables': tables,
        'eksemplar_count': eksemplar_count,
        'sirkulasi_count': sirkulasi_count
    })
'''
# append to end
code += debug_api

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Debug tables API added.")
