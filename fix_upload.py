import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    content = f.read()

# Replace the old file.save logic with the new one
old_logic = '''        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join('static', filename)
            file.save(filepath)
            
            try:
                df = pd.read_excel(filepath)'''

new_logic = '''        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join('/tmp', filename) if os.name != 'nt' else filename
            
            try:
                file.save(filepath)
                df = pd.read_excel(filepath)'''

content = content.replace(old_logic, new_logic)

# Also fix the 500 error in analisis_lanjutan if the table doesn't exist yet!
old_analisis = '''    # 1. Turnover Rate per DDC Class'''
new_analisis = '''    # Pastikan tabel peminjaman ada agar tidak 500 error
    try:
        conn.execute('SELECT 1 FROM peminjaman LIMIT 1')
    except:
        return redirect(url_for('import_slims'))

    # 1. Turnover Rate per DDC Class'''

content = content.replace(old_analisis, new_analisis)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(content)

print("Fixes applied")
