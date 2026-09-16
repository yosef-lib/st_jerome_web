import codecs
import re

with codecs.open('app.py', 'r', 'utf-8') as f:
    content = f.read()

pattern = re.compile(r"@app\.route\('/analisis_lanjutan'\)\n@login_required\ndef analisis_lanjutan\(\):.*?return render_template\('analisis_lanjutan\.html'.*?\)", re.DOTALL)

new_func = '''@app.route('/analisis_lanjutan')
@login_required
def analisis_lanjutan():
    lokasi = request.args.get('lokasi')
    if not lokasi:
        return render_template('pilih_lokasi.html', mode='analisis_lanjutan')
        
    conn = database.get_db_connection()
    
    try:
        conn.execute('SELECT 1 FROM peminjaman LIMIT 1')
    except:
        return redirect(url_for('import_slims'))

    # 1. Turnover Rate (existing)
    turnover_query = """
        SELECT 
            CASE 
                WHEN SUBSTR(b.klasifikasi, 1, 1) = '0' THEN '000 - Komputer & Informasi'
                WHEN SUBSTR(b.klasifikasi, 1, 1) = '1' THEN '100 - Filsafat & Psikologi'
                WHEN SUBSTR(b.klasifikasi, 1, 1) = '2' THEN '200 - Agama & Teologi'
                WHEN SUBSTR(b.klasifikasi, 1, 1) = '3' THEN '300 - Ilmu Sosial'
                WHEN SUBSTR(b.klasifikasi, 1, 1) = '4' THEN '400 - Bahasa'
                WHEN SUBSTR(b.klasifikasi, 1, 1) = '5' THEN '500 - Sains & Matematika'
                WHEN SUBSTR(b.klasifikasi, 1, 1) = '6' THEN '600 - Teknologi'
                WHEN SUBSTR(b.klasifikasi, 1, 1) = '7' THEN '700 - Kesenian & Rekreasi'
                WHEN SUBSTR(b.klasifikasi, 1, 1) = '8' THEN '800 - Sastra'
                WHEN SUBSTR(b.klasifikasi, 1, 1) = '9' THEN '900 - Sejarah & Geografi'
                ELSE 'Lainnya'
            END as ddc_group,
            COUNT(DISTINCT b.no_induk) as total_eksemplar,
            COUNT(DISTINCT p.id) as total_pinjam
        FROM buku b
        LEFT JOIN peminjaman p ON b.no_induk = p.Kode Eksemplar
        WHERE b.lokasi = ?
        GROUP BY ddc_group
    """
    turnover_data = conn.execute(turnover_query, (lokasi,)).fetchall()

    # 2. Smart Procurement: High Usage, Single Copy
    smart_procurement = conn.execute("""
        WITH Copies AS (
            SELECT judul, pengarang, klasifikasi, COUNT(no_induk) as total_eksemplar
            FROM buku
            WHERE lokasi = ?
            GROUP BY judul, pengarang
            HAVING total_eksemplar = 1
        ),
        InHouseReads AS (
            SELECT b.judul, COUNT(bd.id) as read_count
            FROM buku_dibaca bd
            JOIN buku b ON bd.no_induk = b.no_induk
            WHERE b.lokasi = ?
            GROUP BY b.judul
        ),
        ExternalLoans AS (
            SELECT p.Judul as judul, COUNT(p.id) as loan_count
            FROM peminjaman p
            GROUP BY p.Judul
        )
        SELECT 
            c.judul, 
            c.pengarang,
            c.klasifikasi,
            c.total_eksemplar,
            COALESCE(i.read_count, 0) as read_count,
            COALESCE(e.loan_count, 0) as loan_count,
            (COALESCE(i.read_count, 0) + COALESCE(e.loan_count, 0)) as total_usage
        FROM Copies c
        LEFT JOIN InHouseReads i ON c.judul = i.judul
        LEFT JOIN ExternalLoans e ON c.judul = e.judul
        WHERE total_usage > 2
        ORDER BY total_usage DESC
        LIMIT 10
    """, (lokasi, lokasi)).fetchall()

    # 3. Gap Subjek Prioritas
    gap_subjek = conn.execute("""
        SELECT 
            CASE 
                WHEN SUBSTR(klasifikasi, 1, 1) = '0' THEN '000 - Komputer & Informasi'
                WHEN SUBSTR(klasifikasi, 1, 1) = '1' THEN '100 - Filsafat & Psikologi'
                WHEN SUBSTR(klasifikasi, 1, 1) = '2' THEN '200 - Agama & Teologi'
                WHEN SUBSTR(klasifikasi, 1, 1) = '3' THEN '300 - Ilmu Sosial'
                WHEN SUBSTR(klasifikasi, 1, 1) = '4' THEN '400 - Bahasa'
                WHEN SUBSTR(klasifikasi, 1, 1) = '5' THEN '500 - Sains & Matematika'
                WHEN SUBSTR(klasifikasi, 1, 1) = '6' THEN '600 - Teknologi'
                WHEN SUBSTR(klasifikasi, 1, 1) = '7' THEN '700 - Kesenian & Rekreasi'
                WHEN SUBSTR(klasifikasi, 1, 1) = '8' THEN '800 - Sastra'
                WHEN SUBSTR(klasifikasi, 1, 1) = '9' THEN '900 - Sejarah & Geografi'
                ELSE 'Lainnya'
            END as ddc_group,
            MAX(tgl_terima) as update_terakhir,
            COUNT(no_induk) as jumlah_koleksi
        FROM buku
        WHERE lokasi = ? AND tgl_terima IS NOT NULL AND tgl_terima != ''
        GROUP BY ddc_group
        ORDER BY update_terakhir ASC
        LIMIT 5
    """, (lokasi,)).fetchall()

    # 4. Akreditasi: Judul & Eksemplar
    akreditasi_judul_eks = conn.execute('SELECT COUNT(DISTINCT judul) as j, COUNT(no_induk) as e FROM buku WHERE lokasi = ?', (lokasi,)).fetchone()
    
    # 5. Akreditasi: Inti vs Umum
    akreditasi_inti_umum = conn.execute("""
        SELECT 
            SUM(CASE WHEN SUBSTR(klasifikasi, 1, 1) IN ('1', '2') THEN 1 ELSE 0 END) as inti,
            SUM(CASE WHEN SUBSTR(klasifikasi, 1, 1) NOT IN ('1', '2') THEN 1 ELSE 0 END) as umum,
            COUNT(*) as total
        FROM buku WHERE lokasi = ?
    """, (lokasi,)).fetchone()

    # 6. Akreditasi: Pertambahan / Tahun
    akreditasi_pertambahan = conn.execute("""
        SELECT SUBSTR(tgl_terima, 1, 4) as tahun, COUNT(no_induk) as jumlah 
        FROM buku WHERE lokasi = ? AND tgl_terima IS NOT NULL AND tgl_terima != ''
        GROUP BY tahun ORDER BY tahun DESC LIMIT 3
    """, (lokasi,)).fetchall()

    return render_template('analisis_lanjutan.html', 
                          lokasi=lokasi, 
                          turnover_data=turnover_data,
                          smart_procurement=smart_procurement,
                          gap_subjek=gap_subjek,
                          akr_je=akreditasi_judul_eks,
                          akr_iu=akreditasi_inti_umum,
                          akr_tambah=akreditasi_pertambahan)'''

content = pattern.sub(new_func, content)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(content)
print("app.py analisis_lanjutan updated")
