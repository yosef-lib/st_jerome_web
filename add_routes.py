import codecs

new_route = '''

@app.route('/analisis_lanjutan')
@login_required
def analisis_lanjutan():
    lokasi = request.args.get('lokasi')
    if not lokasi:
        return redirect(url_for('pilih_lokasi', mode='analisis_lanjutan'))
        
    conn = database.get_db_connection()
    
    # 1. Turnover Rate per DDC Class
    turnover_query = """
        SELECT 
            CASE 
                WHEN SUBSTR(b.klasifikasi, 1, 1) = '0' THEN '000 - Komputer & Informasi'
                WHEN SUBSTR(b.klasifikasi, 1, 1) = '1' THEN '100 - Filsafat & Psikologi'
                WHEN SUBSTR(b.klasifikasi, 1, 1) = '2' THEN '200 - Agama & Teologi'
                WHEN SUBSTR(b.klasifikasi, 1, 1) = '3' THEN '300 - Ilmu Sosial'
                WHEN SUBSTR(b.klasifikasi, 1, 1) = '4' THEN '400 - Bahasa'
                WHEN SUBSTR(b.klasifikasi, 1, 1) = '5' THEN '500 - Sains'
                WHEN SUBSTR(b.klasifikasi, 1, 1) = '6' THEN '600 - Teknologi'
                WHEN SUBSTR(b.klasifikasi, 1, 1) = '7' THEN '700 - Seni & Rekreasi'
                WHEN SUBSTR(b.klasifikasi, 1, 1) = '8' THEN '800 - Sastra'
                WHEN SUBSTR(b.klasifikasi, 1, 1) = '9' THEN '900 - Sejarah & Geografi'
                ELSE 'Lainnya'
            END as kategori,
            COUNT(DISTINCT b.no_induk) as total_eksemplar,
            COUNT(p.id) as total_peminjaman,
            ROUND(CAST(COUNT(p.id) AS FLOAT) / CAST(NULLIF(COUNT(DISTINCT b.no_induk), 0) AS FLOAT), 2) as turnover
        FROM buku b
        LEFT JOIN peminjaman p ON b.no_induk = p.no_induk
        WHERE b.lokasi = ?
        GROUP BY SUBSTR(b.klasifikasi, 1, 1)
        ORDER BY turnover DESC
    """
    turnover_data = conn.execute(turnover_query, (lokasi,)).fetchall()
    
    # 2. Dead Stock (Koleksi Dorman) - Tidak pernah dipinjam & tidak pernah dibaca di meja
    dead_stock_query = """
        SELECT b.no_induk, b.judul, b.pengarang, b.klasifikasi
        FROM buku b
        LEFT JOIN peminjaman p ON b.no_induk = p.no_induk
        LEFT JOIN buku_dibaca bd ON b.no_induk = bd.no_induk
        WHERE b.lokasi = ? AND p.id IS NULL AND bd.id IS NULL
        ORDER BY b.id ASC
        LIMIT 50
    """
    dead_stock_data = conn.execute(dead_stock_query, (lokasi,)).fetchall()
    
    # 3. In-House vs Out-of-House
    in_house_count = conn.execute('SELECT COUNT(*) FROM buku_dibaca bd JOIN buku b ON bd.no_induk = b.no_induk WHERE b.lokasi = ?', (lokasi,)).fetchone()[0]
    out_house_count = conn.execute('SELECT COUNT(*) FROM peminjaman p JOIN buku b ON p.no_induk = b.no_induk WHERE b.lokasi = ?', (lokasi,)).fetchone()[0]
    
    conn.close()
    
    return render_template('analisis_lanjutan.html', 
                           lokasi=lokasi,
                           turnover_data=turnover_data,
                           dead_stock_data=dead_stock_data,
                           in_house_count=in_house_count,
                           out_house_count=out_house_count)
'''

with codecs.open('app.py', 'r', 'utf-8') as f:
    content = f.read()

content = content.replace("if __name__ == '__main__':", new_route + "\nif __name__ == '__main__':")

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(content)
print("Route added")
