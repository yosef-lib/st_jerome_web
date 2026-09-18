import codecs
import re

# 1. Update app.py cetak routes
with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

# Fix cetak_sirkulasi query
old_cetak_s = '''    if search:
        query = 'SELECT * FROM buku WHERE judul LIKE ? OR pengarang LIKE ? OR no_induk LIKE ? ORDER BY id DESC LIMIT ? OFFSET ?'
        params = (f'%{search}%', f'%{search}%', f'%{search}%', per_page, offset)
        count_query = 'SELECT COUNT(*) FROM buku WHERE judul LIKE ? OR pengarang LIKE ? OR no_induk LIKE ?'
        count_params = (f'%{search}%', f'%{search}%', f'%{search}%')
    else:
        query = 'SELECT * FROM buku ORDER BY id DESC LIMIT ? OFFSET ?'
        params = (per_page, offset)
        count_query = 'SELECT COUNT(*) FROM buku'
    
    total_books = conn.execute(count_query, count_params if search else ()).fetchone()[0]
    buku_list = conn.execute(query, params).fetchall()'''

new_cetak_s = '''    if search:
        query = 'SELECT e.no_induk, b.judul, b.pengarang, b.penerbit, b.tahun_terbit, b.klasifikasi, b.no_panggil FROM eksemplar e JOIN bibliografi b ON e.biblio_id = b.id WHERE b.judul LIKE ? OR b.pengarang LIKE ? OR e.no_induk LIKE ? ORDER BY e.no_induk DESC LIMIT ? OFFSET ?'
        params = (f'%{search}%', f'%{search}%', f'%{search}%', per_page, offset)
        count_query = 'SELECT COUNT(*) FROM eksemplar e JOIN bibliografi b ON e.biblio_id = b.id WHERE b.judul LIKE ? OR b.pengarang LIKE ? OR e.no_induk LIKE ?'
        count_params = (f'%{search}%', f'%{search}%', f'%{search}%')
    else:
        query = 'SELECT e.no_induk, b.judul, b.pengarang, b.penerbit, b.tahun_terbit, b.klasifikasi, b.no_panggil FROM eksemplar e JOIN bibliografi b ON e.biblio_id = b.id ORDER BY e.no_induk DESC LIMIT ? OFFSET ?'
        params = (per_page, offset)
        count_query = 'SELECT COUNT(*) FROM eksemplar'
    
    total_books = conn.execute(count_query, count_params if search else ()).fetchone()[0]
    buku_list = conn.execute(query, params).fetchall()'''

code = code.replace(old_cetak_s, new_cetak_s)

# Fix api_cetak_sirkulasi query
old_api_cetak_s = '''    if ids:
        buku_list_raw = conn.execute(f'SELECT * FROM buku WHERE id IN ({placeholders})', ids).fetchall()
        buku_list = [dict(row) for row in buku_list_raw]'''

new_api_cetak_s = '''    if ids:
        buku_list_raw = conn.execute(f'SELECT e.no_induk, b.judul, b.pengarang, b.klasifikasi, b.no_panggil as cutter FROM eksemplar e JOIN bibliografi b ON e.biblio_id = b.id WHERE e.no_induk IN ({placeholders})', ids).fetchall()
        
        # Parse no_panggil into klasifikasi, cutter, huruf_judul for the sticker template
        buku_list = []
        for row in buku_list_raw:
            d = dict(row)
            parts = d.get('cutter', '').split()
            d['klasifikasi'] = parts[0] if len(parts) > 0 else d.get('klasifikasi', '')
            d['cutter'] = parts[1] if len(parts) > 1 else ''
            d['huruf_judul'] = parts[2] if len(parts) > 2 else ''
            buku_list.append(d)'''

code = code.replace(old_api_cetak_s, new_api_cetak_s)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)

# 2. Update HTML checkboxes
with codecs.open('templates/cetak_sirkulasi.html', 'r', 'utf-8') as f:
    html_code = f.read()

html_code = html_code.replace('value="{{ buku.id }}"', 'value="{{ buku.no_induk }}"')
html_code = html_code.replace("const id = checkbox.value;", "const id = checkbox.value;") # Just making sure

with codecs.open('templates/cetak_sirkulasi.html', 'w', 'utf-8') as f:
    f.write(html_code)

print("Refactored cetak_sirkulasi to use Eksemplar.")
