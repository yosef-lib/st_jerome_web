import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    content = f.read()

# Add dead_stock and in_house back to analisis_lanjutan
old_return = "return render_template('analisis_lanjutan.html', "
new_code = '''
    # 1.5. Dead Stock (Koleksi Dorman)
    dead_stock = conn.execute("""
        SELECT b.judul, b.pengarang, b.klasifikasi
        FROM buku b
        LEFT JOIN buku_dibaca bd ON b.no_induk = bd.no_induk
        LEFT JOIN peminjaman p ON b.no_induk = p.no_induk
        WHERE b.lokasi = ? AND bd.id IS NULL AND p.id IS NULL
        LIMIT 10
    """, (lokasi,)).fetchall()

    # 1.6. In-House vs External
    total_in_house = conn.execute("SELECT COUNT(*) FROM buku_dibaca bd JOIN buku b ON bd.no_induk = b.no_induk WHERE b.lokasi = ?", (lokasi,)).fetchone()[0]
    total_external = conn.execute("SELECT COUNT(*) FROM peminjaman p JOIN buku b ON p.no_induk = b.no_induk WHERE b.lokasi = ?", (lokasi,)).fetchone()[0]

    return render_template('analisis_lanjutan.html', 
                          dead_stock=dead_stock,
                          total_in_house=total_in_house,
                          total_external=total_external,
                          '''

content = content.replace(old_return, new_code)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(content)
print("added old stats")
