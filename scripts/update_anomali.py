import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

# I need to find the SQL query for inkonsistensi in app.py
old_query = '''    inkonsistensi = conn.execute("""
        SELECT a.judul, a.no_induk as no_induk_1, a.klasifikasi as kelas_1, b.no_induk as no_induk_2, b.klasifikasi as kelas_2
        FROM buku a
        JOIN buku b ON a.judul = b.judul AND a.lokasi = b.lokasi AND a.id != b.id
        WHERE a.lokasi = ? AND a.klasifikasi != b.klasifikasi AND a.klasifikasi != '' AND b.klasifikasi != ''
        GROUP BY a.judul
        LIMIT 50
    """, (lokasi,)).fetchall()'''

new_query = '''    inkonsistensi = conn.execute("""
        SELECT a.judul, a.no_induk as no_induk_1, a.klasifikasi as kelas_1, a.no_panggil as panggil_1, b.no_induk as no_induk_2, b.klasifikasi as kelas_2, b.no_panggil as panggil_2
        FROM buku a
        JOIN buku b ON a.judul = b.judul AND a.lokasi = b.lokasi AND a.id != b.id
        WHERE a.lokasi = ? AND a.klasifikasi != b.klasifikasi AND a.klasifikasi != '' AND b.klasifikasi != ''
        GROUP BY a.judul
        LIMIT 50
    """, (lokasi,)).fetchall()'''

app_code = app_code.replace(old_query, new_query)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)

print("SQL updated")

# Update anomali.html
with codecs.open('templates/anomali.html', 'r', 'utf-8') as f:
    html = f.read()

old_tds = '''                            <td class="border-b border-[#eee] py-4 px-4">
                                <span class="font-bold text-black">{{ item.no_induk_1 }}</span><br>
                                <span class="text-sm font-bold text-warning">DDC: {{ item.kelas_1 }}</span>
                            </td>
                            <td class="border-b border-[#eee] py-4 px-4">
                                <span class="font-bold text-black">{{ item.no_induk_2 }}</span><br>
                                <span class="text-sm font-bold text-danger">DDC: {{ item.kelas_2 }}</span>
                            </td>'''

new_tds = '''                            <td class="border-b border-[#eee] py-4 px-4">
                                <span class="font-bold text-black">{{ item.no_induk_1 }}</span><br>
                                <span class="text-xs text-slate-500 font-mono">{{ item.panggil_1 or ('DDC: ' ~ item.kelas_1) }}</span>
                            </td>
                            <td class="border-b border-[#eee] py-4 px-4">
                                <span class="font-bold text-black">{{ item.no_induk_2 }}</span><br>
                                <span class="text-xs text-danger font-bold font-mono">{{ item.panggil_2 or ('DDC: ' ~ item.kelas_2) }}</span>
                            </td>'''

html = html.replace(old_tds, new_tds)

old_th = '''                            <th class="py-3 px-4 font-medium text-black">Eksemplar A & DDC</th>
                            <th class="py-3 px-4 font-medium text-black">Eksemplar B & DDC</th>'''
new_th = '''                            <th class="py-3 px-4 font-medium text-black w-1/4">Eksemplar A & No. Panggil</th>
                            <th class="py-3 px-4 font-medium text-black w-1/4">Eksemplar B & No. Panggil</th>'''
html = html.replace(old_th, new_th)

with codecs.open('templates/anomali.html', 'w', 'utf-8') as f:
    f.write(html)

print("HTML updated")
