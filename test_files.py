import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

debug_api = '''
@app.route('/api/debug/files', methods=['GET'])
def api_debug_files():
    import os
    import database
    
    files_found = []
    
    paths_to_check = [
        '/root/st_jerome_web/katalog.db',
        '/root/katalog.db',
        os.path.join(os.getcwd(), 'katalog.db'),
        os.path.abspath('katalog.db'),
        database.DB_NAME,
        os.path.abspath(database.DB_NAME)
    ]
    
    for p in paths_to_check:
        try:
            if os.path.exists(p):
                size = os.path.getsize(p)
                mtime = os.path.getmtime(p)
                # check if it has bibliografi
                import sqlite3
                conn = sqlite3.connect(p)
                has_bib = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bibliografi'").fetchone() is not None
                conn.close()
                files_found.append({'path': p, 'size': size, 'mtime': mtime, 'has_bibliografi': has_bib})
            else:
                files_found.append({'path': p, 'exists': False})
        except Exception as e:
            files_found.append({'path': p, 'error': str(e)})
            
    return jsonify(files_found)
'''

code += debug_api

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Debug files API added")
