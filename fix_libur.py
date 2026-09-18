import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

# Fix calculate_working_days
old_libur = '''def calculate_working_days(start_date, end_date, conn):
    import datetime
    libur_rows = conn.execute("SELECT tanggal FROM hari_libur").fetchall()
    libur_set = set(row[0] for row in libur_rows)'''
new_libur = '''def calculate_working_days(start_date, end_date, conn):
    import datetime
    try:
        libur_rows = conn.execute("SELECT tanggal FROM hari_libur").fetchall()
        libur_set = set(row[0] for row in libur_rows)
    except:
        libur_set = set()'''
code = code.replace(old_libur, new_libur)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Fixed calculate_working_days.")
