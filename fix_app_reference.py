import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

# Fix api_buku insert
old_insert = \"\"\"            INSERT OR REPLACE INTO buku (
                no_induk, tgl_terima, status_buku, judul, pengarang, subjek, gmd, edisi, 
                isbn, penerbit, tahun_terbit, tempat_terbit, deskripsi_fisik, 
                judul_seri, bahasa, klasifikasi, cutter, huruf_judul, copy_ke, catatan, lokasi
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('no_induk'), data.get('tgl_terima'), data.get('status_buku'),
            data.get('judul'), data.get('pengarang'), data.get('subjek'),
            data.get('gmd'), data.get('edisi'), data.get('isbn'),
            data.get('penerbit'), data.get('tahun_terbit'), data.get('tempat_terbit'),
            data.get('deskripsi_fisik'), data.get('judul_seri'), data.get('bahasa'),
            data.get('klasifikasi'), data.get('cutter'), data.get('huruf_judul'),
            data.get('copy_ke'), data.get('catatan'), data.get('lokasi', 'IMAVI')
        )\"\"\"

new_insert = \"\"\"            INSERT OR REPLACE INTO buku (
                no_induk, tgl_terima, status_buku, judul, pengarang, subjek, gmd, edisi, 
                isbn, penerbit, tahun_terbit, tempat_terbit, deskripsi_fisik, 
                judul_seri, bahasa, klasifikasi, cutter, huruf_judul, copy_ke, catatan, lokasi, is_reference_only
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('no_induk'), data.get('tgl_terima'), data.get('status_buku'),
            data.get('judul'), data.get('pengarang'), data.get('subjek'),
            data.get('gmd'), data.get('edisi'), data.get('isbn'),
            data.get('penerbit'), data.get('tahun_terbit'), data.get('tempat_terbit'),
            data.get('deskripsi_fisik'), data.get('judul_seri'), data.get('bahasa'),
            data.get('klasifikasi'), data.get('cutter'), data.get('huruf_judul'),
            data.get('copy_ke'), data.get('catatan'), data.get('lokasi', 'IMAVI'), 1 if str(data.get('is_reference_only', 'false')).lower() in ['true', '1'] else 0
        )\"\"\"

code = code.replace(old_insert, new_insert)

# Fix edit_koleksi update
old_update = \"\"\"            UPDATE buku SET 
                no_induk=?, judul=?, pengarang=?, subjek=?, gmd=?, edisi=?, 
                isbn=?, penerbit=?, tahun_terbit=?, tempat_terbit=?, deskripsi_fisik=?, 
                judul_seri=?, bahasa=?, klasifikasi=?, cutter=?, huruf_judul=?, lokasi=?
            WHERE id=?
        ''', (
            request.form.get('no_induk'), request.form.get('judul'), request.form.get('pengarang'),
            request.form.get('subjek'), request.form.get('gmd'), request.form.get('edisi'),
            request.form.get('isbn'), request.form.get('penerbit'), request.form.get('tahun_terbit'),
            request.form.get('tempat_terbit'), request.form.get('deskripsi_fisik'), request.form.get('judul_seri'),
            request.form.get('bahasa'), request.form.get('klasifikasi'), request.form.get('cutter'),
            request.form.get('huruf_judul'), request.form.get('lokasi'), id
        )\"\"\"

new_update = \"\"\"            UPDATE buku SET 
                no_induk=?, judul=?, pengarang=?, subjek=?, gmd=?, edisi=?, 
                isbn=?, penerbit=?, tahun_terbit=?, tempat_terbit=?, deskripsi_fisik=?, 
                judul_seri=?, bahasa=?, klasifikasi=?, cutter=?, huruf_judul=?, lokasi=?, is_reference_only=?
            WHERE id=?
        ''', (
            request.form.get('no_induk'), request.form.get('judul'), request.form.get('pengarang'),
            request.form.get('subjek'), request.form.get('gmd'), request.form.get('edisi'),
            request.form.get('isbn'), request.form.get('penerbit'), request.form.get('tahun_terbit'),
            request.form.get('tempat_terbit'), request.form.get('deskripsi_fisik'), request.form.get('judul_seri'),
            request.form.get('bahasa'), request.form.get('klasifikasi'), request.form.get('cutter'),
            request.form.get('huruf_judul'), request.form.get('lokasi'), 1 if request.form.get('is_reference_only') else 0, id
        )\"\"\"

code = code.replace(old_update, new_update)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Updated app.py")
