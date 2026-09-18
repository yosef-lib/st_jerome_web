import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

new_routes = '''@app.route('/manajemen_data')
@login_required
def manajemen_data():
    return render_template('manajemen_data.html')

@app.route('/eksport_stpd')
@login_required
def eksport_stpd():
    import csv, io
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM buku WHERE lokasi = 'STPD'")
    rows = cursor.fetchall()
    
    si = io.StringIO()
    writer = csv.writer(si)
    columns = [description[0] for description in cursor.description]
    writer.writerow(columns)
    writer.writerows(rows)
    conn.close()
    
    output = si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=Data_Buku_STPD.csv"}
    )

@app.route('/hapus_stpd', methods=['POST'])
@login_required
def hapus_stpd():
    conn = database.get_db_connection()
    conn.execute("DELETE FROM buku WHERE lokasi = 'STPD'")
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'message': 'Data STPD berhasil dihapus permanen.'})

# END OF NEW ROUTES
'''

if '/manajemen_data' not in code:
    code = code.replace("if __name__ == '__main__':", new_routes + "\nif __name__ == '__main__':")
    with codecs.open('app.py', 'w', 'utf-8') as f:
        f.write(code)
    print("Routes added")
else:
    print("Routes already exist")
