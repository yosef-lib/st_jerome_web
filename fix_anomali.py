import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

old_anomali = '''    # 2. Inkonsistensi Klasifikasi (Judul sama persis, tapi beda klasifikasi)
    inkonsistensi = conn.execute("""
        SELECT a.judul, a.no_induk as no_induk_1, a.klasifikasi as kelas_1, 
               TRIM(a.klasifikasi || ' ' || COALESCE(a.cutter, '') || ' ' || COALESCE(a.huruf_judul, '')) as panggil_1, 
               b.no_induk as no_induk_2, b.klasifikasi as kelas_2, 
               TRIM(b.klasifikasi || ' ' || COALESCE(b.cutter, '') || ' ' || COALESCE(b.huruf_judul, '')) as panggil_2
        FROM buku a
        JOIN buku b ON a.judul = b.judul AND a.lokasi = b.lokasi AND a.id != b.id
        WHERE a.lokasi = ? AND a.klasifikasi != b.klasifikasi AND a.klasifikasi != '' AND b.klasifikasi != ''
        GROUP BY a.judul
        LIMIT 50
    """, (lokasi,)).fetchall()

    return render_template('anomali.html', lokasi=lokasi, metadata_cacat=metadata_cacat, inkonsistensi=inkonsistensi)'''

new_anomali = '''    # 2. Inkonsistensi Klasifikasi (Judul sama persis, tapi beda klasifikasi)
    page = int(request.args.get('page', 1))
    per_page = 5
    offset = (page - 1) * per_page
    
    # Get total anomalies for pagination
    total_anomalies_query = conn.execute("""
        SELECT COUNT(DISTINCT judul) FROM buku 
        WHERE lokasi = ? AND klasifikasi != ''
        GROUP BY judul
        HAVING COUNT(DISTINCT klasifikasi) > 1
    """, (lokasi,)).fetchall()
    total_pages = (len(total_anomalies_query) // per_page) + (1 if len(total_anomalies_query) % per_page > 0 else 0)
    
    titles_with_inconsistency = conn.execute("""
        SELECT judul FROM buku 
        WHERE lokasi = ? AND klasifikasi != ''
        GROUP BY judul
        HAVING COUNT(DISTINCT klasifikasi) > 1
        LIMIT ? OFFSET ?
    """, (lokasi, per_page, offset)).fetchall()
    
    inkonsistensi_dict = {}
    for t in titles_with_inconsistency:
        judul = t['judul']
        exemplars = conn.execute("""
            SELECT no_induk, judul, klasifikasi, pengarang, penerbit, tahun_terbit,
                   TRIM(klasifikasi || ' ' || COALESCE(cutter, '') || ' ' || COALESCE(huruf_judul, '')) as no_panggil
            FROM buku
            WHERE judul = ? AND lokasi = ?
            ORDER BY no_induk
        """, (judul, lokasi)).fetchall()
        inkonsistensi_dict[judul] = [dict(e) for e in exemplars]

    return render_template('anomali.html', lokasi=lokasi, metadata_cacat=metadata_cacat, inkonsistensi_dict=inkonsistensi_dict, page=page, total_pages=total_pages)'''

app_code = app_code.replace(old_anomali, new_anomali)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)

print("anomali backend fixed")
