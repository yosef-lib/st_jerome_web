import codecs
import re

with codecs.open('app.py', 'r', 'utf-8') as f:
    content = f.read()

new_route = '''
@app.route('/anomali')
@login_required
def anomali():
    lokasi = request.args.get('lokasi', 'STPD')
    conn = database.get_db_connection()
    
    # 1. Metadata Tidak Lengkap
    metadata_cacat = conn.execute("""
        SELECT no_induk, judul, pengarang, klasifikasi 
        FROM buku 
        WHERE lokasi = ? AND 
        (klasifikasi IS NULL OR klasifikasi = '' OR pengarang IS NULL OR pengarang = '' OR judul IS NULL OR judul = '')
        LIMIT 50
    """, (lokasi,)).fetchall()
    
    # 2. Inkonsistensi Klasifikasi (Judul sama persis, tapi beda klasifikasi)
    inkonsistensi = conn.execute("""
        SELECT a.judul, a.no_induk as no_induk_1, a.klasifikasi as kelas_1, b.no_induk as no_induk_2, b.klasifikasi as kelas_2
        FROM buku a
        JOIN buku b ON a.judul = b.judul AND a.lokasi = b.lokasi AND a.id != b.id
        WHERE a.lokasi = ? AND a.klasifikasi != b.klasifikasi AND a.klasifikasi != '' AND b.klasifikasi != ''
        GROUP BY a.judul
        LIMIT 50
    """, (lokasi,)).fetchall()

    return render_template('anomali.html', lokasi=lokasi, metadata_cacat=metadata_cacat, inkonsistensi=inkonsistensi)

if __name__ == '__main__':'''

content = content.replace("if __name__ == '__main__':", new_route)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(content)

# Update layout.html to rename Scanner and add Anomali menu
with codecs.open('templates/layout.html', 'r', 'utf-8') as f:
    layout = f.read()

layout = layout.replace('Scanner Meja Baca', 'Scanner & Audit Rak')

# Add Anomali to sidebar under Analisis Dasar
menu_anomali = '''
            <li>
              <a href="/anomali?lokasi={{ request.args.get('lokasi', 'STPD') }}" class="group relative flex items-center gap-2.5 rounded-sm py-2 px-4 font-medium text-bodydark1 duration-300 ease-in-out hover:bg-graydark dark:hover:bg-meta-4">
                <i class="fa-solid fa-triangle-exclamation"></i>
                Kualitas Data (Anomali)
              </a>
            </li>
'''
layout = layout.replace('<!-- Add more specific menu items here if needed -->', menu_anomali + '\n            <!-- Add more specific menu items here if needed -->')

with codecs.open('templates/layout.html', 'w', 'utf-8') as f:
    f.write(layout)

print("anomali route and layout updated")
