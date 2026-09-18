import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

old_update = """        if image_filename:
            conn.execute("UPDATE bibliografi SET image = ? WHERE id = ?", (image_filename, biblio_id))"""

new_update = """        if image_filename:
            conn.execute("UPDATE bibliografi SET image = ? WHERE id = ?", (image_filename, biblio_id))
        
        # Also update status_buku in all eksemplar
        if data.get('status_buku'):
            conn.execute("UPDATE eksemplar SET status_buku = ? WHERE biblio_id = ?", (data.get('status_buku'), biblio_id))"""

code = code.replace(old_update, new_update)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)

print("Backend patched")
