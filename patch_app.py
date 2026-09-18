import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

old_insert = '''        cursor = conn.execute("""
            INSERT INTO bibliografi (judul, pengarang, penerbit, isbn, klasifikasi, tempat_terbit, tahun_terbit, edisi, bahasa)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get('judul'), data.get('pengarang'), data.get('penerbit'), data.get('isbn'),
            data.get('klasifikasi'), data.get('tempat_terbit'), data.get('tahun_terbit'),
            data.get('edisi'), data.get('bahasa', 'Indonesia')
        ))'''

new_insert = '''        cursor = conn.execute("""
            INSERT INTO bibliografi (
                judul, pengarang, penerbit, isbn, klasifikasi, tempat_terbit, 
                tahun_terbit, edisi, bahasa, gmd, deskripsi_fisik, judul_seri, 
                cutter, huruf_judul, subjek
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get('judul'), data.get('pengarang'), data.get('penerbit'), data.get('isbn'),
            data.get('klasifikasi'), data.get('tempat_terbit'), data.get('tahun_terbit'),
            data.get('edisi'), data.get('bahasa', 'Indonesia'),
            data.get('gmd', 'Text'), data.get('deskripsi_fisik'), data.get('judul_seri'),
            data.get('cutter'), data.get('huruf_judul'), data.get('subjek')
        ))'''

code = code.replace(old_insert, new_insert)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Patched app.py")
