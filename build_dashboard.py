import codecs
import re

with codecs.open('app.py', 'r', 'utf-8') as f:
    content = f.read()

old_dashboard = '''@app.route('/dashboard')
@login_required
def dashboard():
    lokasi = request.args.get('lokasi')
    if not lokasi:
        return render_template('pilih_lokasi.html', mode='dashboard')
        
    conn = database.get_db_connection()
    total_buku = conn.execute('SELECT COUNT(*) FROM buku WHERE lokasi = ?', (lokasi,)).fetchone()[0]
    total_baca = conn.execute('SELECT COUNT(*) FROM buku_dibaca bd JOIN buku b ON bd.no_induk = b.no_induk WHERE b.lokasi = ?', (lokasi,)).fetchone()[0]
    
    ddc_data = conn.execute('''
        SELECT substr(klasifikasi, 1, 1) || '00' as ddc_kelas, COUNT(*) as total_count
        FROM buku 
        WHERE klasifikasi IS NOT NULL AND klasifikasi != '' AND lokasi = ?
        GROUP BY ddc_kelas
        ORDER BY total_count DESC
    ''', (lokasi,)).fetchall()
    
    labels = [d['ddc_kelas'] for d in ddc_data]
    data_counts = [d['total_count'] for d in ddc_data]
    
    dominant_author_row = conn.execute('SELECT pengarang, COUNT(*) as c FROM buku WHERE pengarang != "" AND lokasi = ? GROUP BY pengarang ORDER BY c DESC LIMIT 1', (lokasi,)).fetchone()
    dominant_author = dominant_author_row['pengarang'] if dominant_author_row else '-'
    dominant_author_count = dominant_author_row['c'] if dominant_author_row else 0
    
    ddc_distribution = []
    for d in ddc_data:
        code = d['ddc_kelas']
        topik = 'Karya Umum'
        if code == '100': topik = 'Filsafat'
        elif code == '200': topik = 'Agama'
        elif code == '300': topik = 'Ilmu Sosial'
        elif code == '400': topik = 'Bahasa'
        elif code == '500': topik = 'Ilmu Murni'
        elif code == '600': topik = 'Ilmu Terapan'
        elif code == '700': topik = 'Kesenian'
        elif code == '800': topik = 'Kesusastraan'
        elif code == '900': topik = 'Sejarah & Geografi'
        
        ddc_distribution.append({
            'klasifikasi': code,
            'count': d['total_count'],
            'topik': topik
        })

    return render_template('intelijen_evaluasi.html', 
                          lokasi=lokasi, 
                          total_buku=total_buku, 
                          total_baca=total_baca, 
                          dominant_author=dominant_author,
                          dominant_author_count=dominant_author_count,
                          ddc_distribution=ddc_distribution)'''

new_dashboard = '''@app.route('/dashboard')
@login_required
def dashboard():
    lokasi = request.args.get('lokasi')
    if not lokasi:
        return render_template('pilih_lokasi.html', mode='dashboard')
        
    conn = database.get_db_connection()
    
    # 1. Input Hari Ini (today's date in YYYY-MM-DD)
    from datetime import date
    today_str = date.today().strftime('%Y-%m-%d')
    
    input_hari_ini = conn.execute('SELECT COUNT(*) FROM buku WHERE tgl_terima = ? AND lokasi = ?', (today_str, lokasi)).fetchone()[0]
    
    # 2. Dibaca di Meja Baca (today)
    dibaca_hari_ini = conn.execute('SELECT COUNT(*) FROM buku_dibaca bd JOIN buku b ON bd.no_induk = b.no_induk WHERE bd.tanggal = ? AND b.lokasi = ?', (today_str, lokasi)).fetchone()[0]
    
    # 3. Antrean Cetak Label
    import os, json
    antrean_count = 0
    antrean_list = []
    if os.path.exists(ANTREAN_FILE):
        with open(ANTREAN_FILE, 'r') as f:
            try:
                antrean_list = json.load(f)
                antrean_count = len(antrean_list)
            except:
                pass
    
    # Get all no_induk in antrean for quick lookup
    antrean_no_induk = [item.get('no_induk') for item in antrean_list]
    
    # 4. Anomali Metadata (missing DDC or missing Author/Title)
    anomali = conn.execute('''
        SELECT COUNT(*) FROM buku 
        WHERE lokasi = ? AND 
        (klasifikasi IS NULL OR klasifikasi = '' OR pengarang IS NULL OR pengarang = '' OR judul IS NULL OR judul = '')
    ''', (lokasi,)).fetchone()[0]
    
    # 5. Tabel Rekapan Input Hari Ini
    buku_input_hari_ini = conn.execute('''
        SELECT no_induk, judul, klasifikasi 
        FROM buku 
        WHERE tgl_terima = ? AND lokasi = ?
        ORDER BY id DESC LIMIT 20
    ''', (today_str, lokasi)).fetchall()
    
    rekapan_list = []
    for b in buku_input_hari_ini:
        status = 'ANTRE' if b['no_induk'] in antrean_no_induk else 'SIAP'
        rekapan_list.append({
            'no_induk': b['no_induk'],
            'judul': b['judul'],
            'ddc': b['klasifikasi'] if b['klasifikasi'] else '-',
            'status': status
        })
        
    # 6. Buku Paling Sering Dibaca (In-house usage)
    buku_sering_dibaca = conn.execute('''
        SELECT b.judul, b.pengarang, b.klasifikasi, COUNT(bd.id) as freq
        FROM buku_dibaca bd
        JOIN buku b ON bd.no_induk = b.no_induk
        WHERE b.lokasi = ?
        GROUP BY b.no_induk
        ORDER BY freq DESC
        LIMIT 10
    ''', (lokasi,)).fetchall()
    
    return render_template('intelijen_evaluasi.html', 
                          lokasi=lokasi, 
                          input_hari_ini=input_hari_ini,
                          dibaca_hari_ini=dibaca_hari_ini,
                          antrean_count=antrean_count,
                          anomali=anomali,
                          rekapan_list=rekapan_list,
                          buku_sering_dibaca=buku_sering_dibaca)'''

content = content.replace(old_dashboard, new_dashboard)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(content)
print("app.py updated")
