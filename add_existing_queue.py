import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

# Add a route to push existing book to queue
new_route = '''@app.route('/api/antrean/existing', methods=['POST'])
@login_required
def add_antrean_existing():
    data = request.json
    no_induk = data.get('no_induk')
    
    conn = database.get_db_connection()
    buku_db = conn.execute("SELECT * FROM buku WHERE no_induk = ?", (no_induk,)).fetchone()
    conn.close()
    
    if not buku_db:
        return jsonify({'status': 'error', 'message': 'Buku tidak ditemukan di database.'}), 404
        
    buku_dict = dict(buku_db)
    
    # Save to JSON Queue for printing
    import os, json
    ANTREAN_FILE = 'antrian_stiker.json'
    queue = []
    if os.path.exists(ANTREAN_FILE):
        with open(ANTREAN_FILE, 'r') as f:
            try:
                queue = json.load(f)
            except:
                pass
            
    queue.append(buku_dict)
    with open(ANTREAN_FILE, 'w') as f:
        json.dump(queue, f)
        
    return jsonify({'status': 'success', 'data': buku_dict})
'''

# Find the place to inject
anchor = "@app.route('/cetak_pdf')"
code = code.replace(anchor, new_route + '\n' + anchor)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)

print("added route")
