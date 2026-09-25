import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

# Update the POST API logic to include fakultas
old_api = '''        # Simpan log
        conn.execute("""
            INSERT INTO sjla_visitor_logs (tipe_pengunjung, identitas, asal_instansi, peran_jabatan)
            VALUES (?, ?, ?, ?)
        """, (tipe_pengunjung, identitas, asal_instansi, peran))
        conn.commit()'''

new_api = '''        # Simpan log
        fakultas = data.get('fakultas', '').strip()
        try:
            conn.execute("ALTER TABLE sjla_visitor_logs ADD COLUMN fakultas TEXT")
        except:
            pass
            
        conn.execute("""
            INSERT INTO sjla_visitor_logs (tipe_pengunjung, identitas, asal_instansi, peran_jabatan, fakultas)
            VALUES (?, ?, ?, ?, ?)
        """, (tipe_pengunjung, identitas, asal_instansi, peran, fakultas))
        conn.commit()'''

app_code = app_code.replace(old_api, new_api)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)

print("API updated for fakultas")
