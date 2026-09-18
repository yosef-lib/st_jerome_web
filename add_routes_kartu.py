import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

new_routes = '''
@app.route('/cetak_kartu')
@login_required
def cetak_kartu():
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
        
    buku_list = conn.execute(query, params).fetchall()
    total_books = conn.execute(count_query, count_params).fetchone()[0]
    conn.close()
    
    total_pages = (total_books + per_page - 1) // per_page
    return render_template('cetak_kartu.html', buku_list=buku_list, page=page, total_pages=total_pages, search=search)

@app.route('/api/cetak_kartu', methods=['POST'])
@login_required
def api_cetak_kartu():
    import json, os, tempfile
    from template_stiker import generate_stiker_pdf
    
    data = request.json
    ids = data.get('ids', [])
    options = data.get('options', {})
    
    conn = database.get_db_connection()
    buku_list = []
    for no_induk in ids:
        b = conn.execute('SELECT * FROM buku WHERE no_induk = ?', (no_induk,)).fetchone()
        if b: buku_list.append(dict(b))
    conn.close()
    
    if not buku_list:
        return "Tidak ada buku yang dipilih", 400
        
    fd, temp_path = tempfile.mkstemp(suffix='.json')
    with os.fdopen(fd, 'w') as f:
        json.dump(buku_list, f)
        
    output_pdf = 'kartu_buku_output.pdf'
    if os.path.exists(output_pdf): os.remove(output_pdf)
    
    try:
        generate_stiker_pdf(temp_path, output_pdf, options)
        os.remove(temp_path)
        return send_file(output_pdf, as_attachment=True, download_name='kartu_kantong.pdf')
    except Exception as e:
        print("Error generating PDF:", e)
        if os.path.exists(temp_path): os.remove(temp_path)
        return "Gagal menghasilkan PDF.", 500
'''

anchor = "@app.route('/cetak_pdf')"
app_code = app_code.replace(anchor, new_routes + '\n' + anchor)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)
print("app.py routes added")
