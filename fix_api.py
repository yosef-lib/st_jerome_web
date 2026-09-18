import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

old_loop = '''    conn = database.get_db_connection()
    buku_list = []
    for no_induk in ids:
        b = conn.execute('SELECT * FROM buku WHERE no_induk = ?', (no_induk,)).fetchone()
        if b: buku_list.append(dict(b))
    conn.close()'''

new_loop = '''    conn = database.get_db_connection()
    placeholders = ','.join('?' for _ in ids)
    buku_list = []
    if ids:
        buku_list_raw = conn.execute(f'SELECT * FROM buku WHERE id IN ({placeholders})', ids).fetchall()
        buku_list = [dict(row) for row in buku_list_raw]
    conn.close()'''

app_code = app_code.replace(old_loop, new_loop)

# Also fix the search form action in cetak_sirkulasi.html!
with codecs.open('templates/cetak_sirkulasi.html', 'r', 'utf-8') as f:
    html = f.read()
html = html.replace('action="/cetak_khusus"', 'action="/cetak_sirkulasi"')
with codecs.open('templates/cetak_sirkulasi.html', 'w', 'utf-8') as f:
    f.write(html)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)
