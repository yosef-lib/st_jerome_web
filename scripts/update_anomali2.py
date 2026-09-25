import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

# Fix the query to concatenate klasifikasi, cutter, huruf_judul
old_query = '''    inkonsistensi = conn.execute("""
        SELECT a.judul, a.no_induk as no_induk_1, a.klasifikasi as kelas_1, a.no_panggil as panggil_1, b.no_induk as no_induk_2, b.klasifikasi as kelas_2, b.no_panggil as panggil_2
        FROM buku a
        JOIN buku b ON a.judul = b.judul AND a.lokasi = b.lokasi AND a.id != b.id
        WHERE a.lokasi = ? AND a.klasifikasi != b.klasifikasi AND a.klasifikasi != '' AND b.klasifikasi != ''
        GROUP BY a.judul
        LIMIT 50
    """, (lokasi,)).fetchall()'''

new_query = '''    inkonsistensi = conn.execute("""
        SELECT a.judul, a.no_induk as no_induk_1, a.klasifikasi as kelas_1, 
               TRIM(a.klasifikasi || ' ' || COALESCE(a.cutter, '') || ' ' || COALESCE(a.huruf_judul, '')) as panggil_1, 
               b.no_induk as no_induk_2, b.klasifikasi as kelas_2, 
               TRIM(b.klasifikasi || ' ' || COALESCE(b.cutter, '') || ' ' || COALESCE(b.huruf_judul, '')) as panggil_2
        FROM buku a
        JOIN buku b ON a.judul = b.judul AND a.lokasi = b.lokasi AND a.id != b.id
        WHERE a.lokasi = ? AND a.klasifikasi != b.klasifikasi AND a.klasifikasi != '' AND b.klasifikasi != ''
        GROUP BY a.judul
        LIMIT 50
    """, (lokasi,)).fetchall()'''

app_code = app_code.replace(old_query, new_query)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)

print("SQL fixed")
