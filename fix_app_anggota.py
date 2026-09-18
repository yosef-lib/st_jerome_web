import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

old_edit = '''@app.route('/edit_anggota', methods=['POST'])
@login_required
def edit_anggota():
    member_id = request.form.get('member_id')
    nama = request.form.get('nama')
    tipe_anggota = request.form.get('tipe_anggota')
    masa_berlaku = request.form.get('masa_berlaku')
    
    if member_id and nama and tipe_anggota and masa_berlaku:
        conn = database.get_db_connection()
        conn.execute('UPDATE anggota SET nama=?, tipe_anggota=?, masa_berlaku=? WHERE member_id=?',
                     (nama, tipe_anggota, masa_berlaku, member_id))
        conn.commit()
        conn.close()'''

new_edit = '''@app.route('/edit_anggota', methods=['POST'])
@login_required
def edit_anggota():
    member_id = request.form.get('member_id')
    nama = request.form.get('nama')
    tipe_anggota = request.form.get('tipe_anggota')
    masa_berlaku = request.form.get('masa_berlaku')
    status = request.form.get('status', 'AKTIF')
    
    if member_id and nama and tipe_anggota and masa_berlaku:
        conn = database.get_db_connection()
        conn.execute('UPDATE anggota SET nama=?, tipe_anggota=?, masa_berlaku=?, status=? WHERE member_id=?',
                     (nama, tipe_anggota, masa_berlaku, status, member_id))
        conn.commit()
        conn.close()'''

code = code.replace(old_edit, new_edit)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Updated edit_anggota route in app.py")
