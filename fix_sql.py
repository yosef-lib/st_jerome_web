import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

# Fix api_renew
old_renew = '''SELECT s.*, e.member_id as e_member_id, a.tipe_anggota'''
new_renew = '''SELECT s.*, s.member_id as e_member_id, a.tipe_anggota'''
code = code.replace(old_renew, new_renew)

# Fix api_return
old_return = '''loan = conn.execute("SELECT s.*, e.member_id as e_member_id, a.nama as anggota_nama, b.judul FROM sirkulasi s JOIN eksemplar e ON s.no_induk = e.no_induk JOIN bibliografi b ON e.biblio_id = b.id LEFT JOIN anggota a ON s.member_id = a.member_id WHERE s.no_induk = ? AND s.return_date IS NULL", (book_id,)).fetchone()'''
new_return = '''loan = conn.execute("SELECT s.*, s.member_id as e_member_id, a.nama as anggota_nama, b.judul FROM sirkulasi s JOIN eksemplar e ON s.no_induk = e.no_induk JOIN bibliografi b ON e.biblio_id = b.id LEFT JOIN anggota a ON s.member_id = a.member_id WHERE s.no_induk = ? AND s.return_date IS NULL", (book_id,)).fetchone()'''
code = code.replace(old_return, new_return)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Fixed SQL queries.")
