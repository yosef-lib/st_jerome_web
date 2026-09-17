from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file, session, flash
import csv
import database
import json
import os
import io
from functools import wraps

app = Flask(__name__)
app.secret_key = 'stjerome_secret_key'
ANTREAN_FILE = 'antrian_stiker.json'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Inisialisasi database jika belum ada
if not os.path.exists(database.DB_NAME):
    database.init_db()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'yosef' and request.form['password'] == 'bcajember':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Username atau Password salah')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/cetak_stiker')
@login_required
def cetak_stiker():
    return render_template('input_stiker.html')

@app.route('/api/antrean', methods=['GET'])
@login_required
def get_antrean():
    if os.path.exists(ANTREAN_FILE):
        with open(ANTREAN_FILE, 'r') as f:
            try:
                return jsonify(json.load(f))
            except:
                return jsonify([])
    return jsonify([])

@app.route('/api/antrean', methods=['POST'])
@login_required
def add_antrean():
    data = request.json
    
    # Save to SQLite DB
    conn = database.get_db_connection()
    try:
        conn.execute('''
            INSERT OR REPLACE INTO buku (
                no_induk, tgl_terima, status_buku, judul, pengarang, subjek, gmd, edisi, 
                isbn, penerbit, tahun_terbit, tempat_terbit, deskripsi_fisik, 
                judul_seri, bahasa, klasifikasi, cutter, huruf_judul, copy_ke, catatan, lokasi
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('no_induk'), data.get('tgl_terima'), data.get('status_buku'),
            data.get('judul'), data.get('pengarang'), data.get('subjek'),
            data.get('gmd'), data.get('edisi'), data.get('isbn'),
            data.get('penerbit'), data.get('tahun_terbit'), data.get('tempat_terbit'),
            data.get('deskripsi_fisik'), data.get('judul_seri'), data.get('bahasa'),
            data.get('klasifikasi'), data.get('cutter'), data.get('huruf_judul'),
            data.get('copy_ke'), data.get('catatan'), data.get('lokasi', 'STPD')
        ))
        conn.commit()
    except Exception as e:
        print("Error DB:", e)
    finally:
        conn.close()

    # Save to JSON Queue for printing
    queue = []
    if os.path.exists(ANTREAN_FILE):
        with open(ANTREAN_FILE, 'r') as f:
            try:
                queue = json.load(f)
            except:
                pass
            
    queue.append(data)
    with open(ANTREAN_FILE, 'w') as f:
        json.dump(queue, f)
        
    return jsonify({'status': 'success'})

@app.route('/api/antrean/hapus', methods=['POST'])
@login_required
def hapus_antrean():
    index = request.json.get('index')
    if os.path.exists(ANTREAN_FILE):
        with open(ANTREAN_FILE, 'r') as f:
            queue = json.load(f)
        if 0 <= index < len(queue):
            queue.pop(index)
            with open(ANTREAN_FILE, 'w') as f:
                json.dump(queue, f)
    return jsonify({'status': 'success'})

@app.route('/api/antrean/hapus_semua', methods=['POST'])
@login_required
def hapus_semua_antrean():
    if os.path.exists(ANTREAN_FILE):
        os.remove(ANTREAN_FILE)
    return jsonify({'status': 'success'})

@app.route('/cetak_pdf')
@login_required
def cetak_pdf():
    import template_stiker
    success = template_stiker.generate_stiker_pdf()
    if success:
        return send_file('stiker_output.pdf', as_attachment=True)
    return "Gagal membuat PDF atau antrean kosong.", 400

@app.route('/export_baca')
@login_required
def export_baca():
    conn = database.get_db_connection()
    # Export by current month if needed, but for now we export all grouped by klasifikasi
    data = conn.execute('''
        SELECT b.klasifikasi, b.no_induk, b.judul, b.pengarang, COUNT(bd.id) as total_baca 
        FROM buku_dibaca bd 
        JOIN buku b ON bd.no_induk = b.no_induk 
        GROUP BY b.no_induk 
        ORDER BY b.klasifikasi ASC, total_baca DESC
    ''').fetchall()
    conn.close()
    
    output = io.StringIO()
    writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Klasifikasi DDC', 'No Induk', 'Judul Buku', 'Pengarang', 'Total Dibaca'])
    
    for row in data:
        writer.writerow([row['klasifikasi'], row['no_induk'], row['judul'], row['pengarang'], row['total_baca']])
        
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        mimetype="text/csv",
        as_attachment=True,
        download_name="Laporan_Baca_Buku.csv"
    )

@app.route('/export_biblio')
@login_required
def export_biblio():
    import slims_bridge
    csv_str = slims_bridge.generate_biblio_csv()
    return send_file(
        io.BytesIO(csv_str.encode('utf-8-sig')),
        mimetype="text/csv",
        as_attachment=True,
        download_name="biblio_export.csv"
    )

@app.route('/export_item')
@login_required
def export_item():
    import slims_bridge
    csv_str = slims_bridge.generate_item_csv()
    return send_file(
        io.BytesIO(csv_str.encode('utf-8-sig')),
        mimetype="text/csv",
        as_attachment=True,
        download_name="item_export.csv"
    )

@app.route('/scan')
@login_required
def scan():
    return render_template('scan_baca.html')

@app.route('/api/scan', methods=['POST'])
def api_scan():
    data = request.json
    no_induk = data.get('no_induk')
    
    if not no_induk:
        return jsonify({'status': 'error', 'message': 'Barcode kosong'})
        
    conn = database.get_db_connection()
    buku = conn.execute('SELECT judul, subjek FROM buku WHERE no_induk = ?', (no_induk,)).fetchone()
    
    if buku:
        conn.execute('INSERT OR REPLACE INTO buku_dibaca (no_induk) VALUES (?)', (no_induk,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'judul': buku['judul'], 'subjek': buku['subjek']})
    else:
        conn.close()
        return jsonify({'status': 'error', 'message': f'Buku dengan No Induk {no_induk} tidak ditemukan.'})

@app.route('/dashboard')
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
    anomali = conn.execute("""
        SELECT COUNT(*) FROM buku 
        WHERE lokasi = ? AND 
        (klasifikasi IS NULL OR klasifikasi = '' OR pengarang IS NULL OR pengarang = '' OR judul IS NULL OR judul = '')
    """, (lokasi,)).fetchone()[0]
    
    # 5. Tabel Rekapan Input Hari Ini
    buku_input_hari_ini = conn.execute("""
        SELECT no_induk, judul, klasifikasi 
        FROM buku 
        WHERE tgl_terima = ? AND lokasi = ?
        ORDER BY id DESC LIMIT 20
    """, (today_str, lokasi)).fetchall()
    
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
    buku_sering_dibaca = conn.execute("""
        SELECT b.judul, b.pengarang, b.klasifikasi, COUNT(bd.id) as freq
        FROM buku_dibaca bd
        JOIN buku b ON bd.no_induk = b.no_induk
        WHERE b.lokasi = ?
        GROUP BY b.no_induk
        ORDER BY freq DESC
        LIMIT 10
    """, (lokasi,)).fetchall()
    
    return render_template('intelijen_evaluasi.html', 
                          lokasi=lokasi, 
                          input_hari_ini=input_hari_ini,
                          dibaca_hari_ini=dibaca_hari_ini,
                          antrean_count=antrean_count,
                          anomali=anomali,
                          rekapan_list=rekapan_list,
                          buku_sering_dibaca=buku_sering_dibaca)

@app.route('/koleksi')
@login_required
def daftar_koleksi():
    lokasi = request.args.get('lokasi')
    if not lokasi:
        # Jika belum milih lokasi, tampilkan halaman pilih lokasi
        return render_template('pilih_lokasi.html', mode='koleksi')
        
    conn = database.get_db_connection()
    page = int(request.args.get('page', 1))
    search = request.args.get('search', '')
    limit = 50
    offset = (page - 1) * limit
    
    if search:
        query = 'SELECT * FROM buku WHERE lokasi = ? AND (judul LIKE ? OR no_induk LIKE ? OR pengarang LIKE ?) ORDER BY id DESC LIMIT ? OFFSET ?'
        buku_list = conn.execute(query, (lokasi, f'%{search}%', f'%{search}%', f'%{search}%', limit, offset)).fetchall()
        total = conn.execute('SELECT COUNT(*) FROM buku WHERE lokasi = ? AND (judul LIKE ? OR no_induk LIKE ? OR pengarang LIKE ?)', (lokasi, f'%{search}%', f'%{search}%', f'%{search}%')).fetchone()[0]
    else:
        buku_list = conn.execute('SELECT * FROM buku WHERE lokasi = ? ORDER BY id DESC LIMIT ? OFFSET ?', (lokasi, limit, offset)).fetchall()
        total = conn.execute('SELECT COUNT(*) FROM buku WHERE lokasi = ?', (lokasi,)).fetchone()[0]
        
    conn.close()
    
    total_pages = (total + limit - 1) // limit
    
    return render_template('koleksi.html', 
                           buku_list=buku_list, 
                           page=page, 
                           total_pages=total_pages,
                           search=search,
                           lokasi=lokasi)

@app.route('/koleksi/delete/<int:id>', methods=['POST'])
@login_required
def delete_koleksi(id):
    conn = database.get_db_connection()
    conn.execute('DELETE FROM buku WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('daftar_koleksi'))

@app.route('/koleksi/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_koleksi(id):
    conn = database.get_db_connection()
    buku = conn.execute('SELECT * FROM buku WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        conn.execute('''
            UPDATE buku SET 
                no_induk=?, judul=?, pengarang=?, subjek=?, gmd=?, edisi=?, 
                isbn=?, penerbit=?, tahun_terbit=?, tempat_terbit=?, deskripsi_fisik=?, 
                judul_seri=?, bahasa=?, klasifikasi=?, cutter=?, huruf_judul=?, lokasi=?
            WHERE id=?
        ''', (
            request.form.get('no_induk'), request.form.get('judul'), request.form.get('pengarang'),
            request.form.get('subjek'), request.form.get('gmd'), request.form.get('edisi'),
            request.form.get('isbn'), request.form.get('penerbit'), request.form.get('tahun_terbit'),
            request.form.get('tempat_terbit'), request.form.get('deskripsi_fisik'), request.form.get('judul_seri'),
            request.form.get('bahasa'), request.form.get('klasifikasi'), request.form.get('cutter'),
            request.form.get('huruf_judul'), request.form.get('lokasi'), id
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('daftar_koleksi'))
        
    conn.close()
    return render_template('edit_koleksi.html', buku=buku)

@app.route('/anggota')
@login_required
def daftar_anggota():
    conn = database.get_db_connection()
    search = request.args.get('search', '')
    
    if search:
        query = 'SELECT * FROM anggota WHERE nama LIKE ? OR member_id LIKE ? ORDER BY id DESC'
        anggota_list = conn.execute(query, (f'%{search}%', f'%{search}%')).fetchall()
    else:
        anggota_list = conn.execute('SELECT * FROM anggota ORDER BY id DESC').fetchall()
        
    conn.close()
    return render_template('anggota.html', anggota_list=anggota_list, search=search)

@app.route('/edit_anggota', methods=['POST'])
@login_required
def edit_anggota():
    member_id = request.form.get('member_id')
    nama = request.form.get('nama')
    tipe_anggota = request.form.get('tipe_anggota')
    masa_berlaku = request.form.get('masa_berlaku')
    
    if member_id and nama and tipe_anggota and masa_berlaku:
        conn = database.get_db_connection()
        conn.execute('''
            UPDATE anggota 
            SET nama = ?, tipe_anggota = ?, masa_berlaku = ?
            WHERE member_id = ?
        ''', (nama, tipe_anggota, masa_berlaku, member_id))
        conn.commit()
        conn.close()
        
    return redirect(url_for('daftar_anggota'))

@app.route('/import_anggota', methods=['POST'])
@login_required
def import_anggota():
    if 'file' not in request.files:
        return redirect(url_for('daftar_anggota'))
        
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('daftar_anggota'))
        
    if file:
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.reader(stream, delimiter=',', quotechar='"')
        
        conn = database.get_db_connection()
        added = 0
        updated = 0
        
        for row in reader:
            if len(row) < 10:
                continue
            
            member_id = row[0]
            nama = row[1]
            tipe = row[3]
            email = row[4]
            alamat = row[5]
            institusi = row[7]
            telepon = row[11] if len(row) > 11 else ''
            masa_berlaku = row[15] if len(row) > 15 else ''
            
            existing = conn.execute('SELECT member_id FROM anggota WHERE member_id = ?', (member_id,)).fetchone()
            
            if existing:
                conn.execute('''
                    UPDATE anggota 
                    SET nama=?, tipe_anggota=?, institusi=?, email=?, telepon=?, alamat=?, masa_berlaku=?
                    WHERE member_id=?
                ''', (nama, tipe, institusi, email, telepon, alamat, masa_berlaku, member_id))
                updated += 1
            else:
                conn.execute('''
                    INSERT INTO anggota (member_id, nama, tipe_anggota, institusi, email, telepon, alamat, masa_berlaku)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (member_id, nama, tipe, institusi, email, telepon, alamat, masa_berlaku))
                added += 1
                
        conn.commit()
        conn.close()
        
    return redirect(url_for('daftar_anggota'))

@app.route('/cetak_kartu', methods=['POST'])
@login_required
def cetak_kartu():
    member_ids = request.form.getlist('member_ids')
    if not member_ids:
        return redirect(url_for('daftar_anggota'))
        
    conn = database.get_db_connection()
    # Build query
    placeholders = ','.join('?' for _ in member_ids)
    query = f"SELECT * FROM anggota WHERE member_id IN ({placeholders})"
    anggota_data = conn.execute(query, member_ids).fetchall()
    conn.close()
    
    import template_kartu
    
    # Convert Row to dict
    anggota_dicts = []
    for a in anggota_data:
        anggota_dicts.append({
            'member_id': a['member_id'],
            'nama': a['nama'],
            'tipe_anggota': a['tipe_anggota'],
            'masa_berlaku': a['masa_berlaku']
        })
        
    template_kartu.generate_cards_pdf(anggota_dicts, 'kartu_output.pdf')
    return send_file('kartu_output.pdf', as_attachment=True)

@app.route('/backup')
@login_required
def backup_db():
    if os.path.exists(database.DB_NAME):
        return send_file(database.DB_NAME, as_attachment=True)
    return "Database belum ada.", 404



@app.route('/analisis_lanjutan')
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
        LEFT JOIN peminjaman p ON b.no_induk = p.no_induk
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
            SELECT p.judul as judul, COUNT(p.id) as loan_count
            FROM peminjaman p
            GROUP BY p.judul
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

    
    # 1.5. Dead Stock (Koleksi Dorman)
    dead_stock = conn.execute("""
        SELECT b.judul, b.pengarang, b.klasifikasi
        FROM buku b
        LEFT JOIN buku_dibaca bd ON b.no_induk = bd.no_induk
        LEFT JOIN peminjaman p ON b.no_induk = p.no_induk
        WHERE b.lokasi = ? AND bd.id IS NULL AND p.id IS NULL
        LIMIT 10
    """, (lokasi,)).fetchall()

    # 1.6. In-House vs External
    total_in_house = conn.execute("SELECT COUNT(*) FROM buku_dibaca bd JOIN buku b ON bd.no_induk = b.no_induk WHERE b.lokasi = ?", (lokasi,)).fetchone()[0]
    total_external = conn.execute("SELECT COUNT(*) FROM peminjaman p JOIN buku b ON p.no_induk = b.no_induk WHERE b.lokasi = ?", (lokasi,)).fetchone()[0]

    return render_template('analisis_lanjutan.html', 
                          dead_stock=dead_stock,
                          total_in_house=total_in_house,
                          total_external=total_external,
                          
                          lokasi=lokasi, 
                          turnover_data=turnover_data,
                          smart_procurement=smart_procurement,
                          gap_subjek=gap_subjek,
                          akr_je=akreditasi_judul_eks,
                          akr_iu=akreditasi_inti_umum,
                          akr_tambah=akreditasi_pertambahan)


import pandas as pd
import os
from werkzeug.utils import secure_filename

@app.route('/import_slims', methods=['GET'])
@login_required
def import_slims():
    return render_template('import_slims.html')

@app.route('/import_slims_loan', methods=['POST'])
@login_required
def import_slims_loan():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
        
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join('/tmp', filename) if os.name != 'nt' else filename
        
        try:
            file.save(filepath)
            df = pd.read_excel(filepath)
            conn = database.get_db_connection()
            
            conn.execute("""
            CREATE TABLE IF NOT EXISTS peminjaman (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id TEXT,
                member_name TEXT,
                no_induk TEXT,
                judul TEXT,
                loan_date TEXT,
                due_date TEXT,
                loan_status TEXT
            )
            """)
            conn.execute('DELETE FROM peminjaman')
            
            for index, row in df.iterrows():
                no_induk = str(row.get('Item Code', ''))
                if no_induk == 'nan' or pd.isna(row.get('Item Code')): no_induk = ''
                
                loan_date = str(row.get('Loan Date', ''))
                if loan_date == 'nan' or pd.isna(row.get('Loan Date')): loan_date = ''
                
                conn.execute("""
                    INSERT INTO peminjaman (member_id, member_name, no_induk, judul, loan_date, due_date, loan_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(row.get('Member ID', '')),
                    str(row.get('Member Name', '')),
                    no_induk,
                    str(row.get('Title', '')),
                    loan_date,
                    str(row.get('Due Date', '')),
                    str(row.get('Loan Status', ''))
                ))
            conn.commit()
            conn.close()
            os.remove(filepath)
            return "<script>alert('Sukses sinkronisasi Riwayat Peminjaman!'); window.location.href='/analisis_lanjutan?lokasi=IMAVI';</script>"
        except Exception as e:
            return f"Error memproses file: {str(e)}", 500

@app.route('/import_slims_katalog', methods=['POST'])
@login_required
def import_slims_katalog():
    biblio_file = request.files.get('biblio_file')
    item_file = request.files.get('item_file')
    
    if not biblio_file or not item_file or biblio_file.filename == '' or item_file.filename == '':
        return "Harap unggah kedua file CSV (Biblio dan Item)!", 400
        
    try:
        import os
        biblio_path = os.path.join('/tmp', 'temp_biblio.csv') if os.name != 'nt' else 'temp_biblio.csv'
        item_path = os.path.join('/tmp', 'temp_item.csv') if os.name != 'nt' else 'temp_item.csv'
        
        biblio_file.save(biblio_path)
        item_file.save(item_path)
        
        import csv
        import re
        
        biblio_map = {}
        with open(biblio_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            headers = next(reader, None)
            for row in reader:
                if len(row) < 18: continue
                title = row[0]
                gmd = row[1]
                edisi = row[2]
                isbn = row[3]
                penerbit = row[4]
                tahun_terbit = row[5]
                deskripsi = row[6]
                klasifikasi = row[11]
                pengarang = row[15].strip('<>').replace('><', ', ')
                subjek = row[16].strip('<>').replace('><', ', ')
                
                item_code_raw = row[17]
                codes = re.findall(r'<(.*?)>', item_code_raw)
                if not codes and item_code_raw.strip():
                    codes = [item_code_raw.strip()]
                
                for code in codes:
                    biblio_map[code] = {
                        'title': title, 'gmd': gmd, 'edisi': edisi, 'isbn': isbn,
                        'penerbit': penerbit, 'tahun_terbit': tahun_terbit,
                        'deskripsi': deskripsi, 'klasifikasi': klasifikasi,
                        'pengarang': pengarang, 'subjek': subjek
                    }
                    
        conn = database.get_db_connection()
        conn.execute('DELETE FROM buku')
        
        count = 0
        with open(item_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            headers = next(reader, None)
            for row in reader:
                if len(row) < 10: continue
                no_induk = row[0]
                call_number = row[1]
                tgl_terima = row[4]
                lokasi_raw = row[7].upper()
                status_buku = row[9]
                
                lokasi = 'IMAVI' if 'IMAVI' in lokasi_raw else ('STPD' if 'STPD' in lokasi_raw else 'UMUM')
                
                bib = biblio_map.get(no_induk, {})
                judul = bib.get('title', row[18] if len(row) > 18 else '')
                pengarang = bib.get('pengarang', '')
                subjek = bib.get('subjek', '')
                gmd = bib.get('gmd', '')
                edisi = bib.get('edisi', '')
                isbn = bib.get('isbn', '')
                penerbit = bib.get('penerbit', '')
                tahun_terbit = bib.get('tahun_terbit', '')
                deskripsi = bib.get('deskripsi', '')
                klasifikasi = bib.get('klasifikasi', '')
                
                parts = call_number.split(' ') if call_number else []
                final_class = parts[0] if len(parts) > 0 else klasifikasi
                cutter = parts[1] if len(parts) > 1 else ''
                huruf = parts[2] if len(parts) > 2 else ''
                
                conn.execute("""
                    INSERT OR REPLACE INTO buku (no_induk, judul, pengarang, lokasi, klasifikasi, cutter, huruf_judul, subjek,
                                    gmd, edisi, isbn, penerbit, tahun_terbit, tempat_terbit, 
                                    deskripsi_fisik, status_buku, tgl_terima)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (no_induk, judul, pengarang, lokasi, final_class, cutter, huruf, subjek,
                      gmd, edisi, isbn, penerbit, tahun_terbit, '', 
                      deskripsi, status_buku, tgl_terima))
                count += 1
                
        conn.commit()
        conn.close()
        
        try: os.remove(biblio_path)
        except: pass
        try: os.remove(item_path)
        except: pass
        
        return f"<script>alert('Sukses sinkronisasi {count} Katalog Buku SLiMS!'); window.location.href='/analisis_lanjutan?lokasi=IMAVI';</script>"
        
    except Exception as e:
        return f"Error memproses file: {str(e)}", 500


@app.route('/export_akreditasi')
@login_required
def export_akreditasi():
    lokasi = request.args.get('lokasi', 'STPD')
    conn = database.get_db_connection()
    
    # Gathering data
    akreditasi_judul_eks = conn.execute('SELECT COUNT(DISTINCT judul) as j, COUNT(no_induk) as e FROM buku WHERE lokasi = ?', (lokasi,)).fetchone()
    akreditasi_inti_umum = conn.execute("""
        SELECT 
            SUM(CASE WHEN SUBSTR(klasifikasi, 1, 1) IN ('1', '2') THEN 1 ELSE 0 END) as inti,
            SUM(CASE WHEN SUBSTR(klasifikasi, 1, 1) NOT IN ('1', '2') THEN 1 ELSE 0 END) as umum,
            COUNT(*) as total
        FROM buku WHERE lokasi = ?
    """, (lokasi,)).fetchone()
    
    # Create an excel file using pandas
    import pandas as pd
    from io import BytesIO
    from flask import send_file
    
    data = [
        {'Indikator': 'Jumlah Judul', 'Nilai': akreditasi_judul_eks['j']},
        {'Indikator': 'Jumlah Eksemplar', 'Nilai': akreditasi_judul_eks['e']},
        {'Indikator': 'Koleksi Inti (Teologi/Filsafat)', 'Nilai': akreditasi_inti_umum['inti']},
        {'Indikator': 'Koleksi Umum', 'Nilai': akreditasi_inti_umum['umum']},
        {'Indikator': 'Total Koleksi', 'Nilai': akreditasi_inti_umum['total']}
    ]
    
    df = pd.DataFrame(data)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Borang Akreditasi')
    
    output.seek(0)
    
    return send_file(
        output, 
        as_attachment=True, 
        download_name=f'Borang_Akreditasi_{lokasi}.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


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
    page = int(request.args.get('page', 1))
    per_page = 5
    offset = (page - 1) * per_page
    
    # Get total anomalies for pagination
    total_anomalies_query = conn.execute("""
        SELECT COUNT(DISTINCT judul) FROM buku 
        WHERE lokasi = ? AND klasifikasi != ''
        GROUP BY judul
        HAVING COUNT(DISTINCT klasifikasi) > 1
    """, (lokasi,)).fetchall()
    total_pages = (len(total_anomalies_query) // per_page) + (1 if len(total_anomalies_query) % per_page > 0 else 0)
    
    titles_with_inconsistency = conn.execute("""
        SELECT judul FROM buku 
        WHERE lokasi = ? AND klasifikasi != ''
        GROUP BY judul
        HAVING COUNT(DISTINCT klasifikasi) > 1
        LIMIT ? OFFSET ?
    """, (lokasi, per_page, offset)).fetchall()
    
    inkonsistensi_dict = {}
    for t in titles_with_inconsistency:
        judul = t['judul']
        exemplars = conn.execute("""
            SELECT no_induk, judul, klasifikasi, pengarang, penerbit, tahun_terbit,
                   TRIM(klasifikasi || ' ' || COALESCE(cutter, '') || ' ' || COALESCE(huruf_judul, '')) as no_panggil
            FROM buku
            WHERE judul = ? AND lokasi = ?
            ORDER BY no_induk
        """, (judul, lokasi)).fetchall()
        inkonsistensi_dict[judul] = [dict(e) for e in exemplars]

    return render_template('anomali.html', lokasi=lokasi, metadata_cacat=metadata_cacat, inkonsistensi_dict=inkonsistensi_dict, page=page, total_pages=total_pages)


@app.route('/audit_rak')
@login_required
def audit_rak():
    conn = database.get_db_connection()
    riwayat = conn.execute("""
        SELECT a.waktu_scan, a.rak_target, a.status_audit, b.no_induk, b.judul, b.klasifikasi
        FROM audit_rak a
        JOIN buku b ON a.no_induk = b.no_induk
        ORDER BY a.id DESC LIMIT 100
    """).fetchall()
    
    # Statistik
    stats = conn.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN status_audit = 'BENAR' THEN 1 ELSE 0 END) as benar,
            SUM(CASE WHEN status_audit = 'SALAH RAK' THEN 1 ELSE 0 END) as salah,
            SUM(CASE WHEN status_audit = 'ANOMALI' THEN 1 ELSE 0 END) as anomali
        FROM audit_rak
    """).fetchone()
    
    return render_template('audit_rak.html', riwayat=riwayat, stats=stats)

@app.route('/export_audit')
@login_required
def export_audit():
    import pandas as pd
    from io import BytesIO
    from flask import send_file
    
    conn = database.get_db_connection()
    df = pd.read_sql_query("""
        SELECT a.waktu_scan as 'Waktu Scan', a.no_induk as 'No Induk', b.judul as 'Judul Buku', a.rak_target as 'Target Rak', a.status_audit as 'Status', b.klasifikasi as 'DDC Seharusnya'
        FROM audit_rak a
        JOIN buku b ON a.no_induk = b.no_induk
        ORDER BY a.id DESC
    """, conn)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Riwayat Audit')
    
    output.seek(0)
    
    return send_file(
        output, 
        as_attachment=True, 
        download_name='Laporan_Audit_Rak.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )



# ==========================================
# BUKU TAMU PENGUNJUNG (KIOSK)
# ==========================================

@app.route('/kiosk')
def kiosk():
    # Halaman Kiosk bersifat publik (tanpa login_required) untuk ditaruh di lobi
    return render_template('kiosk.html')

@app.route('/api/kunjungan/autocomplete', methods=['GET'])
def kunjungan_autocomplete():
    q = request.args.get('q', '').strip()
    if not q or len(q) < 3:
        return jsonify([])
        
    conn = database.get_db_connection()
    try:
        results = conn.execute("""
            SELECT identitas, asal_instansi, peran_jabatan, fakultas 
            FROM sjla_visitor_logs 
            WHERE tipe_pengunjung = 'Non-Member' AND identitas LIKE ?
            GROUP BY identitas
            LIMIT 10
        """, ('%' + q + '%',)).fetchall()
        
        suggestions = [dict(row) for row in results]
        return jsonify(suggestions)
    finally:
        conn.close()

@app.route('/api/kunjungan', methods=['POST'])
def submit_kunjungan():
    data = request.json
    tipe_pengunjung = data.get('tipe_pengunjung', 'Non-Member')
    identitas = data.get('identitas', '').strip()
    asal_instansi = data.get('asal_instansi', '').strip()
    peran = data.get('peran_jabatan', '').strip()
    
    if not identitas:
        return jsonify({"status": "error", "message": "Identitas tidak boleh kosong!"}), 400
        
    conn = database.get_db_connection()
    try:
        # Safeguard if column doesn't exist for some reason
        try:
            conn.execute("ALTER TABLE sjla_visitor_logs ADD COLUMN peran_jabatan TEXT")
        except:
            pass
            
        member_name = None
        if tipe_pengunjung == 'Member':
            # Verifikasi ID di tabel anggota
            member = conn.execute("SELECT nama, institusi FROM anggota WHERE member_id = ?", (identitas,)).fetchone()
            if member:
                member_name = member['nama']
                asal_instansi = member['institusi'] or 'Internal'
            else:
                return jsonify({"status": "error", "message": f"Member dengan ID {identitas} tidak ditemukan."}), 404
        
        # Simpan log
        fakultas = data.get('fakultas', '').strip()
        try:
            conn.execute("ALTER TABLE sjla_visitor_logs ADD COLUMN fakultas TEXT")
        except:
            pass
            
        conn.execute("""
            INSERT INTO sjla_visitor_logs (tipe_pengunjung, identitas, asal_instansi, peran_jabatan, fakultas)
            VALUES (?, ?, ?, ?, ?)
        """, (tipe_pengunjung, identitas, asal_instansi, peran, fakultas))
        conn.commit()
        
        display_name = member_name if member_name else identitas
        return jsonify({
            "status": "success", 
            "message": f"Selamat datang, {display_name}!",
            "display_name": display_name
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()




# ==========================================
# ANALITIK KUNJUNGAN (FASE 2)
# ==========================================

@app.route('/analitik_kunjungan')
@login_required
def analitik_kunjungan():
    conn = database.get_db_connection()
    try:
        # Metrik 1: Kunjungan Hari Ini
        hari_ini_row = conn.execute("""
            SELECT 
                COUNT(id) as total,
                SUM(CASE WHEN tipe_pengunjung = 'Member' THEN 1 ELSE 0 END) as member_count,
                SUM(CASE WHEN tipe_pengunjung = 'Non-Member' THEN 1 ELSE 0 END) as non_member_count
            FROM sjla_visitor_logs 
            WHERE date(waktu_kunjungan) = date('now', 'localtime')
        """).fetchone()
        kunjungan_hari_ini = hari_ini_row['total'] if hari_ini_row else 0
        member_hari_ini = hari_ini_row['member_count'] if hari_ini_row and hari_ini_row['member_count'] else 0
        non_member_hari_ini = hari_ini_row['non_member_count'] if hari_ini_row and hari_ini_row['non_member_count'] else 0
        
        # Metrik 2: Fakultas Hari Ini
        fakultas_today_rows = conn.execute("""
            SELECT fakultas, COUNT(id) as jumlah
            FROM sjla_visitor_logs
            WHERE date(waktu_kunjungan) = date('now', 'localtime') 
              AND fakultas IS NOT NULL AND fakultas != ''
            GROUP BY fakultas
            ORDER BY jumlah DESC
        """).fetchall()
        fakultas_hari_ini = [dict(row) for row in fakultas_today_rows]
        
        # Log Kunjungan Hari Ini
        log_hari_ini_rows = conn.execute("""
            SELECT waktu_kunjungan, identitas, tipe_pengunjung, asal_instansi, peran_jabatan, fakultas
            FROM sjla_visitor_logs
            WHERE date(waktu_kunjungan) = date('now', 'localtime')
            ORDER BY waktu_kunjungan DESC
        """).fetchall()
        log_hari_ini = [dict(row) for row in log_hari_ini_rows]
        
        # Metrik 3: Demografi Instansi (Bulan Ini)
        demografi_rows = conn.execute("""
            SELECT asal_instansi, COUNT(id) as jumlah 
            FROM sjla_visitor_logs 
            WHERE strftime('%Y-%m', waktu_kunjungan) = strftime('%Y-%m', 'now', 'localtime')
            GROUP BY asal_instansi
            ORDER BY jumlah DESC
        """).fetchall()
        demografi = [dict(row) for row in demografi_rows]
        
        # Metrik 3: Top 10 Pengunjung (Bulan Ini)
        top_visitors = conn.execute("""
            SELECT identitas, tipe_pengunjung, asal_instansi, peran_jabatan, fakultas, COUNT(id) as jumlah_kunjungan
            FROM sjla_visitor_logs 
            WHERE strftime('%Y-%m', waktu_kunjungan) = strftime('%Y-%m', 'now', 'localtime')
            GROUP BY identitas
            ORDER BY jumlah_kunjungan DESC
            LIMIT 10
        """).fetchall()
        
    finally:
        conn.close()
        
    return render_template('analitik_kunjungan.html', 
                          kunjungan_hari_ini=kunjungan_hari_ini, 
                          member_hari_ini=member_hari_ini,
                          non_member_hari_ini=non_member_hari_ini,
                          fakultas_hari_ini=fakultas_hari_ini,
                          demografi=demografi, 
                          top_visitors=top_visitors,
                          log_hari_ini=log_hari_ini)

@app.route('/export_kunjungan', methods=['POST'])
@login_required
def export_kunjungan():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    
    if not start_date or not end_date:
        flash('Pilih rentang tanggal terlebih dahulu.', 'danger')
        return redirect(url_for('analitik_kunjungan'))
        
    conn = database.get_db_connection()
    query = """
        SELECT 
            waktu_kunjungan as 'Waktu Kunjungan',
            identitas as 'Nama/ID Pengunjung',
            tipe_pengunjung as 'Status Member',
            asal_instansi as 'Instansi',
            peran_jabatan as 'Peran/Jabatan',
            fakultas as 'Fakultas'
        FROM sjla_visitor_logs
        WHERE date(waktu_kunjungan) >= ? AND date(waktu_kunjungan) <= ?
        ORDER BY waktu_kunjungan DESC
    """
    df = pd.read_sql_query(query, conn, params=(start_date, end_date))
    conn.close()
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Laporan Kunjungan')
    
    output.seek(0)
    
    return send_file(
        output, 
        as_attachment=True, 
        download_name=f'Laporan_Kunjungan_{start_date}_sd_{end_date}.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
