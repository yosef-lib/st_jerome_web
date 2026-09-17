import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

new_routes = '''
@app.route('/cetak_khusus')
@login_required
def cetak_khusus():
    search = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    per_page = 15
    offset = (page - 1) * per_page
    
    conn = database.get_db_connection()
    if search:
        query = 'SELECT * FROM buku WHERE judul LIKE ? OR pengarang LIKE ? OR no_induk LIKE ? ORDER BY id DESC LIMIT ? OFFSET ?'
        params = (f'%{search}%', f'%{search}%', f'%{search}%', per_page, offset)
        count_query = 'SELECT COUNT(*) FROM buku WHERE judul LIKE ? OR pengarang LIKE ? OR no_induk LIKE ?'
        count_params = (f'%{search}%', f'%{search}%', f'%{search}%')
    else:
        query = 'SELECT * FROM buku ORDER BY id DESC LIMIT ? OFFSET ?'
        params = (per_page, offset)
        count_query = 'SELECT COUNT(*) FROM buku'
        count_params = ()
        
    koleksi = conn.execute(query, params).fetchall()
    total = conn.execute(count_query, count_params).fetchone()[0]
    conn.close()
    
    total_pages = (total // per_page) + (1 if total % per_page > 0 else 0)
    
    return render_template('cetak_khusus.html', koleksi_list=[dict(row) for row in koleksi], search=search, page=page, total_pages=total_pages)

@app.route('/api/cetak_khusus', methods=['POST'])
@login_required
def api_cetak_khusus():
    import json, os, tempfile
    from template_stiker import generate_stiker_pdf
    
    data = request.json
    ids = data.get('ids', [])
    options = data.get('options', {})
    
    if not ids:
        return jsonify({'status': 'error', 'message': 'Tidak ada buku yang dipilih'}), 400
        
    conn = database.get_db_connection()
    placeholders = ','.join('?' for _ in ids)
    koleksi = conn.execute(f'SELECT * FROM buku WHERE id IN ({placeholders})', ids).fetchall()
    conn.close()
    
    buku_list = [dict(row) for row in koleksi]
    
    # Write to a temp JSON file
    temp_fd, temp_path = tempfile.mkstemp(suffix='.json')
    with os.fdopen(temp_fd, 'w') as f:
        json.dump(buku_list, f)
        
    output_pdf = 'stiker_khusus_output.pdf'
    
    try:
        generate_stiker_pdf(temp_path, output_pdf, options)
        os.remove(temp_path)
        return send_file(output_pdf, as_attachment=True, download_name='stiker_khusus.pdf')
    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

'''

# Inject before /api/antrean
anchor = "@app.route('/api/antrean', methods=['POST'])"
code = code.replace(anchor, new_routes + '\n' + anchor)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)

print("success routes")
