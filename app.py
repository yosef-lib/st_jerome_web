from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file, session, flash
import csv
import database
import json
import os
import io
from functools import wraps

app = Flask(__name__)

def migrate_db():
    conn = database.get_db_connection()
    try:
        # Check if tanggal_input exists
        columns = [row[1] for row in conn.execute("PRAGMA table_info(anggota)").fetchall()]
        if 'tanggal_input' not in columns:
            print("Migrating database: adding tanggal_input to anggota...")
            conn.execute('ALTER TABLE anggota ADD COLUMN tanggal_input TEXT')
            conn.execute("UPDATE anggota SET tanggal_input = date(masa_berlaku, '-4 years') WHERE masa_berlaku IS NOT NULL")
            
        # Phase 1: Stock Opname & Settings tables
        conn.execute('''CREATE TABLE IF NOT EXISTS pengaturan_sistem (
            kunci TEXT PRIMARY KEY,
            nilai TEXT
        )''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS stock_opname_session (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_sesi TEXT NOT NULL,
            start_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            end_date DATETIME,
            status TEXT DEFAULT 'AKTIF'
        )''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS stock_opname_scan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            no_induk TEXT,
            scan_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'DITEMUKAN',
            FOREIGN KEY (session_id) REFERENCES stock_opname_session(id)
        )''')

        conn.commit()
        print("Migration successful.")
    except Exception as e:
        print("Migration error:", e)
    finally:
        conn.close()

migrate_db()


@app.errorhandler(500)
def internal_error(error):
    import traceback
    return jsonify({
        'status': 'error', 
        'message': 'Internal Server Error: ' + str(error),
        'trace': traceback.format_exc()
    }), 500


app.secret_key = 'stjerome_secret_key_imavi_2026'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400 * 7  # 7 days
ANTREAN_FILE = 'antrian_stiker.json'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def api_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return jsonify({'status': 'error', 'message': 'Sesi tidak valid, silakan refresh halaman.'}), 401
        return f(*args, **kwargs)
    return decorated_function



# Inisialisasi database jika belum ada
if not os.path.exists(database.DB_NAME):
    database.init_db()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'yosef' and request.form['password'] == 'bcajember':
            session.permanent = True
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
def index():
    if 'logged_in' in session:
        return render_template('index.html')
    return redirect(url_for('opac_page'))

@app.route('/opac')
def opac_page():
    return render_template('opac.html')

@app.route('/input_buku')
@login_required
def input_buku():
    return render_template('input_buku.html')

@app.route('/api/antrean', methods=['GET'])
@api_login_required
def get_antrean():
    if os.path.exists(ANTREAN_FILE):
        with open(ANTREAN_FILE, 'r') as f:
            try:
                return jsonify(json.load(f))
            except:
                return jsonify([])
    return jsonify([])


@app.route('/cetak_khusus')
@login_required
def cetak_khusus():
    search = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    per_page = 15
    offset = (page - 1) * per_page
    
    conn = database.get_db_connection()
    if search:
        query = 'SELECT * FROM buku WHERE judul LIKE ? OR pengarang LIKE ? OR no_induk LIKE ? ORDER BY id DESC LIMIT ? OFFSET ?'
        params = (f'%{search}%', f'%{search}%', f'%{search}%', per_page, offset)
        count_query = 'SELECT COUNT(*) FROM buku WHERE judul LIKE ? OR pengarang LIKE ? OR no_induk LIKE ?'
        count_params = (f'%{search}%', f'%{search}%', f'%{search}%')
    else:
        query = 'SELECT * FROM buku ORDER BY id DESC LIMIT ? OFFSET ?'
        params = (per_page, offset)
        count_query = 'SELECT COUNT(*) FROM buku'
        count_params = ()
        
    koleksi = conn.execute(query, params).fetchall()
    total = conn.execute(count_query, count_params).fetchone()[0]
    conn.close()
    
    total_pages = (total // per_page) + (1 if total % per_page > 0 else 0)
    
    return render_template('cetak_khusus.html', koleksi_list=[dict(row) for row in koleksi], search=search, page=page, total_pages=total_pages)

@app.route('/api/cetak_khusus', methods=['POST'])
@api_login_required
def api_cetak_khusus():
    import json, os, tempfile
    from template_stiker import generate_stiker_pdf
    
    data = request.json
    ids = data.get('ids', [])
    options = data.get('options', {})
    
    if not ids:
        return jsonify({'status': 'error', 'message': 'Tidak ada buku yang dipilih'}), 400
        
    conn = database.get_db_connection()
    placeholders = ','.join('?' for _ in ids)
    koleksi_data = conn.execute(f'SELECT * FROM buku WHERE id IN ({placeholders})', ids).fetchall()
    conn.close()
    # Sort to match clicked order
    k_dict = {str(row['id']): row for row in koleksi_data}
    koleksi = [k_dict[str(i)] for i in ids if str(i) in k_dict]
    
    buku_list = [dict(row) for row in koleksi]
    
    # Write to a temp JSON file
    temp_fd, temp_path = tempfile.mkstemp(suffix='.json')
    with os.fdopen(temp_fd, 'w') as f:
        json.dump(buku_list, f)
        
    output_pdf = 'stiker_khusus_output.pdf'
    
    try:
        generate_stiker_pdf(temp_path, output_pdf, options)
        os.remove(temp_path)
        return send_file(output_pdf, as_attachment=True, download_name='stiker_khusus.pdf')
    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': str(e)}), 500



@app.route('/api/buku/<path:no_induk>', methods=['GET'])
@api_login_required
def get_buku(no_induk):
    conn = database.get_db_connection()
    buku = conn.execute("SELECT * FROM buku WHERE no_induk = ?", (no_induk,)).fetchone()
    conn.close()
    
    if buku:
        return jsonify({'status': 'success', 'data': dict(buku)})
    return jsonify({'status': 'error', 'message': 'Not found'}), 404

@app.route('/api/antrean', methods=['POST'])
@api_login_required
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
            data.get('copy_ke'), data.get('catatan'), data.get('lokasi', 'IMAVI')
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
@api_login_required
def hapus_antrean():
    no_induk = request.json.get('no_induk')
    index = request.json.get('index')
    
    if os.path.exists(ANTREAN_FILE):
        import json
        with open(ANTREAN_FILE, 'r') as f:
            try:
                queue = json.load(f)
            except:
                queue = []
                
        if no_induk:
            queue = [b for b in queue if str(b.get('no_induk', '')) != str(no_induk)]
        elif index is not None and 0 <= index < len(queue):
            queue.pop(index)
            
        with open(ANTREAN_FILE, 'w') as f:
            json.dump(queue, f)
            
    return jsonify({'status': 'success'})

@app.route('/api/antrean/hapus_semua', methods=['POST'])
@api_login_required
def hapus_semua_antrean():
    if os.path.exists(ANTREAN_FILE):
        os.remove(ANTREAN_FILE)
    return jsonify({'status': 'success'})

@app.route('/api/antrean/existing', methods=['POST'])
@api_login_required
def add_antrean_existing():
    data = request.json
    no_induk = data.get('no_induk')
    
    conn = database.get_db_connection()
    buku_db = conn.execute("SELECT * FROM buku WHERE no_induk = ?", (no_induk,)).fetchone()
    conn.close()
    
    if not buku_db:
        return jsonify({'status': 'error', 'message': 'Buku tidak ditemukan di database.'}), 404
        
    buku_dict = dict(buku_db)
    
    # Save to JSON Queue for printing
    import os, json
    ANTREAN_FILE = 'antrian_stiker.json'
    queue = []
    if os.path.exists(ANTREAN_FILE):
        with open(ANTREAN_FILE, 'r') as f:
            try:
                queue = json.load(f)
            except:
                pass
            
    queue.append(buku_dict)
    with open(ANTREAN_FILE, 'w') as f:
        json.dump(queue, f)
        
    return jsonify({'status': 'success', 'data': buku_dict})


@app.route('/cetak_sirkulasi')
@login_required
def cetak_sirkulasi():
    search = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    per_page = 15
    offset = (page - 1) * per_page
    
    conn = database.get_db_connection()
    if search:
        query = 'SELECT * FROM buku WHERE judul LIKE ? OR pengarang LIKE ? OR no_induk LIKE ? ORDER BY id DESC LIMIT ? OFFSET ?'
        params = (f'%{search}%', f'%{search}%', f'%{search}%', per_page, offset)
        count_query = 'SELECT COUNT(*) FROM buku WHERE judul LIKE ? OR pengarang LIKE ? OR no_induk LIKE ?'
        count_params = (f'%{search}%', f'%{search}%', f'%{search}%')
    else:
        query = 'SELECT * FROM buku ORDER BY id DESC LIMIT ? OFFSET ?'
        params = (per_page, offset)
        count_query = 'SELECT COUNT(*) FROM buku'
        count_params = ()
        
    buku_list = conn.execute(query, params).fetchall()
    total_books = conn.execute(count_query, count_params).fetchone()[0]
    conn.close()
    
    total_pages = (total_books + per_page - 1) // per_page
    return render_template('cetak_sirkulasi.html', koleksi_list=[dict(row) for row in buku_list], page=page, total_pages=total_pages, search=search)

@app.route('/api/cetak_sirkulasi', methods=['POST'])
@api_login_required
def api_cetak_sirkulasi():
    import json, os, tempfile
    from template_stiker import generate_stiker_pdf
    
    data = request.json
    ids = data.get('ids', [])
    options = data.get('options', {})
    
    conn = database.get_db_connection()
    placeholders = ','.join('?' for _ in ids)
    buku_list = []
    if ids:
        buku_list_raw = conn.execute(f'SELECT e.no_induk, b.judul, b.pengarang, b.klasifikasi, b.no_panggil as cutter FROM eksemplar e JOIN bibliografi b ON e.biblio_id = b.id WHERE e.no_induk IN ({placeholders})', ids).fetchall()
        
        # Parse no_panggil into klasifikasi, cutter, huruf_judul for the sticker template
        buku_list = []
        for row in buku_list_raw:
            d = dict(row)
            parts = d.get('cutter', '').split()
            d['klasifikasi'] = parts[0] if len(parts) > 0 else d.get('klasifikasi', '')
            d['cutter'] = parts[1] if len(parts) > 1 else ''
            d['huruf_judul'] = parts[2] if len(parts) > 2 else ''
            buku_list.append(d)
    conn.close()
    
    if not buku_list:
        return "Tidak ada buku yang dipilih", 400
        
    fd, temp_path = tempfile.mkstemp(suffix='.json')
    with os.fdopen(fd, 'w') as f:
        json.dump(buku_list, f)
        
    output_pdf = 'kartu_buku_output.pdf'
    if os.path.exists(output_pdf): os.remove(output_pdf)
    
    try:
        generate_stiker_pdf(temp_path, output_pdf, options)
        os.remove(temp_path)
        return send_file(output_pdf, as_attachment=True, download_name='kartu_kantong.pdf')
    except Exception as e:
        print("Error generating PDF:", e)
        if os.path.exists(temp_path): os.remove(temp_path)
        return "Gagal menghasilkan PDF.", 500

@app.route('/cetak_pdf')
@login_required
def cetak_pdf():
    from template_stiker import generate_stiker_pdf
    import os
    output_pdf = 'stiker_output.pdf'
    
    if not os.path.exists(ANTREAN_FILE):
        return "Antrean kosong. Tambahkan buku ke antrean terlebih dahulu."
        
    if os.path.exists(output_pdf):
        os.remove(output_pdf)
        
    try:
        generate_stiker_pdf(ANTREAN_FILE, output_pdf)
    except Exception as e:
        print("Error generating PDF:", e)
        return "Gagal menghasilkan PDF. Terjadi kesalahan internal.", 500
    
    if not os.path.exists(output_pdf):
        return "Gagal menghasilkan PDF. Pastikan antrean tidak kosong dan format data benar."
        
    return send_file(output_pdf, as_attachment=True, download_name='stiker.pdf')

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


@app.route('/scan_baca/scanner')
@login_required
def scan_baca_scanner():
    return render_template('scan_baca_scanner.html')

@app.route('/scan')
@login_required
def scan():
    conn = database.get_db_connection()
    # Fetch recently read books today
    recent = conn.execute('''
        SELECT b.judul, e.no_induk, bd.tanggal as waktu
        FROM buku_dibaca bd
        JOIN eksemplar e ON bd.no_induk = e.no_induk
        JOIN bibliografi b ON e.biblio_id = b.id
        WHERE date(bd.tanggal) = date('now', 'localtime')
        ORDER BY bd.tanggal DESC LIMIT 20
    ''').fetchall()
    conn.close()
    return render_template('scan_baca.html', recent=recent)

@app.route('/api/scan', methods=['POST'])
def api_scan():
    data = request.json
    no_induk = data.get('no_induk')
    mode = data.get('mode', 'baca')
    target_rak = data.get('target_rak')
    
    if not no_induk:
        return jsonify({'status': 'error', 'message': 'Barcode kosong'})
        
    conn = database.get_db_connection()
    
    # Gunakan eksemplar JOIN bibliografi
    buku = conn.execute('''
        SELECT e.no_induk, b.judul, b.klasifikasi as subjek 
        FROM eksemplar e 
        JOIN bibliografi b ON e.biblio_id = b.id 
        WHERE e.no_induk = ?
    ''', (no_induk,)).fetchone()
    
    if not buku:
        conn.close()
        return jsonify({'status': 'error', 'message': f'Buku dengan Barcode {no_induk} tidak ditemukan.'})
        
    if mode == 'audit_rak':
        if not target_rak:
            conn.close()
            return jsonify({'status': 'error', 'message': 'Target rak tidak dipilih'})
            
        ddc = str(buku['subjek'] or '')
        status_audit = 'ANOMALI'
        
        # Validasi berdasarkan digit pertama DDC
        if ddc.strip():
            digit_pertama = ddc.strip()[0]
            target_digit = target_rak[0]
            if digit_pertama == target_digit:
                status_audit = 'BENAR'
            else:
                status_audit = 'SALAH RAK'
                
        conn.execute('INSERT INTO audit_rak (no_induk, rak_target, status_audit) VALUES (?, ?, ?)', 
                     (no_induk, target_rak, status_audit))
        conn.commit()
        conn.close()
        # Sesuaikan dengan ekspektasi frontend (success, danger, warning)
        response_status = 'success'
        message = f"Buku {buku['judul']} benar berada di rak ini."
        
        if status_audit == 'SALAH RAK':
            response_status = 'danger'
            message = f"Buku {buku['judul']} (DDC {ddc}) SEHARUSNYA di rak lain!"
        elif status_audit == 'ANOMALI':
            response_status = 'warning'
            message = f"DDC untuk buku {buku['judul']} tidak jelas/kosong."
            
        return jsonify({
            'status': response_status, 
            'judul': buku['judul'], 
            'subjek': ddc,
            'status_audit': status_audit,
            'message': message
        })
    else:
        # Mode Baca
        conn.execute('INSERT OR REPLACE INTO buku_dibaca (no_induk) VALUES (?)', (no_induk,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'judul': buku['judul'], 'subjek': buku['subjek']})

@app.route('/dashboard')
@login_required
def dashboard():
    lokasi = request.args.get('lokasi')
    if not lokasi:
        return redirect(url_for('index', lokasi='IMAVI'))
        
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
        return redirect(url_for('daftar_koleksi', lokasi='IMAVI'))
        
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
                judul_seri=?, bahasa=?, klasifikasi=?, cutter=?, huruf_judul=?, lokasi=?, is_reference_only=?
            WHERE id=?
        ''', (
            request.form.get('no_induk'), request.form.get('judul'), request.form.get('pengarang'),
            request.form.get('subjek'), request.form.get('gmd'), request.form.get('edisi'),
            request.form.get('isbn'), request.form.get('penerbit'), request.form.get('tahun_terbit'),
            request.form.get('tempat_terbit'), request.form.get('deskripsi_fisik'), request.form.get('judul_seri'),
            request.form.get('bahasa'), request.form.get('klasifikasi'), request.form.get('cutter'),
            request.form.get('huruf_judul'), request.form.get('lokasi'), 1 if request.form.get('is_reference_only') else 0, id
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
    tanggal_input = request.form.get('tanggal_input')
    masa_berlaku = request.form.get('masa_berlaku')
    
    if member_id and nama and tipe_anggota and masa_berlaku:
        conn = database.get_db_connection()
        conn.execute('''
            UPDATE anggota 
            SET nama = ?, tipe_anggota = ?, tanggal_input = ?, masa_berlaku = ?
            WHERE member_id = ?
        ''', (nama, tipe_anggota, tanggal_input, masa_berlaku, member_id))
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
    
    # Sort data to match the exact order of selected member_ids from the frontend
    anggota_dict = {row['member_id']: row for row in anggota_data}
    anggota_data = [anggota_dict[m_id] for m_id in member_ids if m_id in anggota_dict]
    
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
        return redirect(url_for('analisis_lanjutan', lokasi='IMAVI'))
        
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
    lokasi = request.args.get('lokasi', 'IMAVI')
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
    lokasi = request.args.get('lokasi', 'IMAVI')
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




@app.route('/audit_rak/scanner')
@login_required
def audit_rak_scanner():
    conn = database.get_db_connection()
    active_session = conn.execute("SELECT * FROM stock_opname_session WHERE status = 'AKTIF' ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()
    if not active_session:
        flash("Tidak ada sesi aktif, silakan mulai sesi terlebih dahulu.", "warning")
        return redirect(url_for('audit_rak'))
    return render_template('audit_rak_scanner.html', active_session=active_session)

@app.route('/audit_rak', methods=['GET', 'POST'])
@login_required
def audit_rak():
    conn = database.get_db_connection()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'start':
            nama_sesi = request.form.get('nama_sesi')
            conn.execute("INSERT INTO stock_opname_session (nama_sesi) VALUES (?)", (nama_sesi,))
            conn.commit()
        elif action == 'stop':
            session_id = request.form.get('session_id')
            conn.execute("UPDATE stock_opname_session SET end_date = CURRENT_TIMESTAMP, status = 'SELESAI' WHERE id = ?", (session_id,))
            conn.commit()
            return redirect(url_for('laporan_opname', session_id=session_id))
            
    # Check active session
    active_session = conn.execute("SELECT * FROM stock_opname_session WHERE status = 'AKTIF' ORDER BY id DESC LIMIT 1").fetchone()
    
    recent_scans = []
    stats = {'total_koleksi': 0, 'ditemukan': 0}
    
    if active_session:
        # Get total koleksi
        stats['total_koleksi'] = conn.execute("SELECT COUNT(*) FROM eksemplar").fetchone()[0]
        # Get found count
        stats['ditemukan'] = conn.execute("SELECT COUNT(DISTINCT no_induk) FROM stock_opname_scan WHERE session_id = ?", (active_session['id'],)).fetchone()[0]
        
        # Get recent 20 scans
        recent_scans = conn.execute('''
            SELECT s.scan_date, s.no_induk, s.status, b.judul 
            FROM stock_opname_scan s
            LEFT JOIN eksemplar e ON s.no_induk = e.no_induk
            LEFT JOIN bibliografi b ON e.biblio_id = b.id
            WHERE s.session_id = ?
            ORDER BY s.id DESC LIMIT 20
        ''', (active_session['id'],)).fetchall()
        
    # Past sessions
    past_sessions = conn.execute("SELECT * FROM stock_opname_session WHERE status = 'SELESAI' ORDER BY id DESC").fetchall()
        
    return render_template('audit_rak.html', active_session=active_session, stats=stats, recent_scans=recent_scans, past_sessions=past_sessions)

@app.route('/api/scan_opname', methods=['POST'])
@login_required
def api_scan_opname():
    data = request.json
    no_induk = data.get('no_induk', '').strip()
    session_id = data.get('session_id')
    target_rak = data.get('target_rak', '')
    
    if not no_induk or not session_id:
        return jsonify({'status': 'error', 'message': 'Data tidak lengkap'})
        
    conn = database.get_db_connection()
    
    # Check if book exists
    buku = conn.execute('''
        SELECT e.no_induk, b.judul, b.klasifikasi
        FROM eksemplar e 
        LEFT JOIN bibliografi b ON e.biblio_id = b.id 
        WHERE e.no_induk = ?
    ''', (no_induk,)).fetchone()
    
    if not buku:
        conn.close()
        return jsonify({'status': 'error', 'message': f'Barcode {no_induk} tidak terdaftar di katalog!'})
        
    # Validate Rak
    ddc = str(buku['klasifikasi'] or '')
    status_rak = 'ANOMALI'
    
    if target_rak == 'F':
        status_rak = 'BENAR' if ddc.upper().startswith('F') else 'SALAH RAK'
    elif target_rak == 'R':
        status_rak = 'BENAR' if ddc.upper().startswith('R') else 'SALAH RAK'
    elif ddc.strip() and target_rak.isdigit():
        digit_pertama = ddc.strip()[0]
        if digit_pertama == target_rak[0]:
            status_rak = 'BENAR'
        else:
            status_rak = 'SALAH RAK'

    # Check if already scanned in this session
    already = conn.execute("SELECT id FROM stock_opname_scan WHERE session_id = ? AND no_induk = ?", (session_id, no_induk)).fetchone()
    if already:
        conn.close()
        return jsonify({
            'status': 'warning', 
            'message': f'Buku {buku["judul"]} sudah dipindai sebelumnya.',
            'no_induk': no_induk,
            'judul': buku['judul'],
            'status_rak': status_rak,
            'ddc_asli': ddc
        })
        
    # Insert with the rack status
    conn.execute("INSERT INTO stock_opname_scan (session_id, no_induk, status) VALUES (?, ?, ?)", (session_id, no_induk, status_rak))
    conn.commit()
    conn.close()
    
    return jsonify({
        'status': 'success',
        'message': f'Berhasil: {buku["judul"]}',
        'no_induk': no_induk,
        'judul': buku['judul'],
        'status_rak': status_rak,
        'ddc_asli': ddc
    })

@app.route('/laporan_opname/<int:session_id>')
@login_required
def laporan_opname(session_id):
    conn = database.get_db_connection()
    sesi = conn.execute("SELECT * FROM stock_opname_session WHERE id = ?", (session_id,)).fetchone()
    if not sesi:
        return "Sesi tidak ditemukan", 404
        
    total_koleksi = conn.execute("SELECT COUNT(*) FROM eksemplar").fetchone()[0]
    ditemukan = conn.execute("SELECT COUNT(DISTINCT no_induk) FROM stock_opname_scan WHERE session_id = ?", (session_id,)).fetchone()[0]
    hilang = total_koleksi - ditemukan
    
    # Ambil 50 buku hilang sebagai sampel
    buku_hilang = conn.execute('''
        SELECT e.no_induk, b.judul, e.lokasi
        FROM eksemplar e
        LEFT JOIN bibliografi b ON e.biblio_id = b.id
        WHERE e.no_induk NOT IN (
            SELECT no_induk FROM stock_opname_scan WHERE session_id = ?
        )
        ORDER BY e.no_induk
        LIMIT 500
    ''', (session_id,)).fetchall()
    
    return render_template('laporan_opname.html', sesi=sesi, total_koleksi=total_koleksi, ditemukan=ditemukan, hilang=hilang, buku_hilang=buku_hilang)




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

from datetime import datetime

@app.route('/analitik_kunjungan')
@login_required
def analitik_kunjungan():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Default: hari ini untuk rentang default jika tidak ada filter
    today_str = datetime.now().strftime('%Y-%m-%d')
    if not start_date:
        start_date = today_str
    if not end_date:
        end_date = today_str
        
    # Jika memfilter rentang bulan, kita bisa memilih tanggal awal bulan hingga akhir bulan.
    # Untuk query kita gunakan: date(waktu_kunjungan) >= start_date AND date(waktu_kunjungan) <= end_date
    
    conn = database.get_db_connection()
    try:
        # Metrik 1: Kunjungan (Filter)
        hari_ini_row = conn.execute("""
            SELECT 
                COUNT(id) as total,
                SUM(CASE WHEN tipe_pengunjung = 'Member' THEN 1 ELSE 0 END) as member_count,
                SUM(CASE WHEN tipe_pengunjung = 'Non-Member' THEN 1 ELSE 0 END) as non_member_count
            FROM sjla_visitor_logs 
            WHERE date(waktu_kunjungan) >= ? AND date(waktu_kunjungan) <= ?
        """, (start_date, end_date)).fetchone()
        kunjungan_hari_ini = hari_ini_row['total'] if hari_ini_row else 0
        member_hari_ini = hari_ini_row['member_count'] if hari_ini_row and hari_ini_row['member_count'] else 0
        non_member_hari_ini = hari_ini_row['non_member_count'] if hari_ini_row and hari_ini_row['non_member_count'] else 0
        
        # Metrik 2: Fakultas (Filter)
        fakultas_today_rows = conn.execute("""
            SELECT fakultas, COUNT(id) as jumlah
            FROM sjla_visitor_logs
            WHERE date(waktu_kunjungan) >= ? AND date(waktu_kunjungan) <= ? 
              AND fakultas IS NOT NULL AND fakultas != ''
            GROUP BY fakultas
            ORDER BY jumlah DESC
        """, (start_date, end_date)).fetchall()
        fakultas_hari_ini = [dict(row) for row in fakultas_today_rows]
        
        # Log Kunjungan (Filter)
        log_hari_ini_rows = conn.execute("""
            SELECT waktu_kunjungan, identitas, tipe_pengunjung, asal_instansi, peran_jabatan, fakultas
            FROM sjla_visitor_logs
            WHERE date(waktu_kunjungan) >= ? AND date(waktu_kunjungan) <= ?
            ORDER BY waktu_kunjungan DESC
        """, (start_date, end_date)).fetchall()
        log_hari_ini = [dict(row) for row in log_hari_ini_rows]
        
        # Metrik 3: Demografi Instansi (Filter)
        demografi_rows = conn.execute("""
            SELECT asal_instansi, COUNT(id) as jumlah 
            FROM sjla_visitor_logs 
            WHERE date(waktu_kunjungan) >= ? AND date(waktu_kunjungan) <= ?
            GROUP BY asal_instansi
            ORDER BY jumlah DESC
        """, (start_date, end_date)).fetchall()
        demografi = [dict(row) for row in demografi_rows]
        
        # Metrik 3: Top 10 Pengunjung (Filter)
        top_visitors = conn.execute("""
            SELECT identitas, tipe_pengunjung, asal_instansi, peran_jabatan, fakultas, COUNT(id) as jumlah_kunjungan
            FROM sjla_visitor_logs 
            WHERE date(waktu_kunjungan) >= ? AND date(waktu_kunjungan) <= ?
            GROUP BY identitas
            ORDER BY jumlah_kunjungan DESC
            LIMIT 10
        """, (start_date, end_date)).fetchall()
        
    finally:
        conn.close()
        
    return render_template('analitik_kunjungan.html', 
                          kunjungan_hari_ini=kunjungan_hari_ini, 
                          member_hari_ini=member_hari_ini,
                          non_member_hari_ini=non_member_hari_ini,
                          fakultas_hari_ini=fakultas_hari_ini,
                          demografi=demografi, 
                          top_visitors=top_visitors,
                          log_hari_ini=log_hari_ini,
                          start_date=start_date,
                          end_date=end_date)

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




@app.route('/sirkulasi')
@login_required
def sirkulasi():
    return render_template('sirkulasi.html', page_title="Sirkulasi & Kasir")


# ==============================================================
# API SIRKULASI (FASE 2)
# ==============================================================

@app.route('/api/sirkulasi/member/<member_id>', methods=['GET'])
@api_login_required
def api_get_member(member_id):
    conn = database.get_db_connection()
    member = conn.execute("SELECT * FROM anggota WHERE member_id = ?", (member_id,)).fetchone()
    if not member:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Anggota tidak ditemukan'})
        
    m = dict(member)
    
    # Hitung pinjaman aktif (buku yang belum dikembalikan)
    active_loans = conn.execute("SELECT COUNT(*) FROM sirkulasi WHERE member_id = ? AND return_date IS NULL", (member_id,)).fetchone()[0]
    
    # Hitung batas maksimal
    tipe = m.get('tipe_anggota', 'Reguler')
    if tipe is None:
        tipe = 'Reguler'
    max_loans = 4 if 'Skripsi' in tipe else 2
    
    # Cek suspend
    import datetime
    if m.get('status') == 'DIBLOKIR' and m.get('suspended_until'):
        suspend_date = datetime.datetime.strptime(m.get('suspended_until'), '%Y-%m-%d').date()
        today = datetime.datetime.now().date()
        if today >= suspend_date:
            conn.execute("UPDATE anggota SET status = ?, suspended_until = ? WHERE member_id = ?", ('AKTIF', None, member_id))
            conn.commit()
            m['status'] = 'AKTIF'
            m['suspended_until'] = None
    
    # Fetch active loans detail
    loans_cursor = conn.execute("""
        SELECT s.*, e.no_induk, b.judul 
        FROM sirkulasi s
        JOIN eksemplar e ON s.no_induk = e.no_induk
        JOIN bibliografi b ON e.biblio_id = b.id
        WHERE s.member_id = ? AND s.return_date IS NULL
    """, (member_id,))
    loans = [dict(row) for row in loans_cursor.fetchall()]

    # Fetch history loans (already returned)
    history_cursor = conn.execute("""
        SELECT s.*, e.no_induk, b.judul 
        FROM sirkulasi s
        JOIN eksemplar e ON s.no_induk = e.no_induk
        JOIN bibliografi b ON e.biblio_id = b.id
        WHERE s.member_id = ? AND s.return_date IS NOT NULL
        ORDER BY s.return_date DESC
    """, (member_id,))
    history_loans = [dict(row) for row in history_cursor.fetchall()]

    conn.close()
    return jsonify({
        'status': 'success',
        'data': {
            'id': m['member_id'],
            'nama': m['nama'],
            'tipe': tipe,
            'status': m['status'],
            'email': m.get('email', '-'),
            'masa_berlaku': m.get('masa_berlaku', '2027-05-07'),
            'suspended_until': m.get('suspended_until', '-'),
            'active_loans': active_loans,
            'max_loans': max_loans,
            'loans': loans,
            'history_loans': history_loans
        }
    })


@app.route('/api/sirkulasi/pay_fine', methods=['POST'])
@api_login_required
def api_pay_fine():
    data = request.json
    loan_id = data.get('loan_id')
    
    conn = database.get_db_connection()
    loan = conn.execute("SELECT * FROM sirkulasi WHERE id = ?", (loan_id,)).fetchone()
    
    if not loan:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Data peminjaman tidak ditemukan.'})
        
    conn.execute("UPDATE sirkulasi SET fine_status = 'LUNAS' WHERE id = ?", (loan_id,))
    
    # Check if user has any OTHER unpaid fines
    unpaid = conn.execute("SELECT COUNT(*) FROM sirkulasi WHERE member_id = ? AND fine_amount > 0 AND fine_status = 'BELUM_LUNAS'", (loan['member_id'],)).fetchone()[0]
    
    if unpaid == 0:
        # Unblock user
        conn.execute("UPDATE anggota SET status = 'AKTIF', suspended_until = NULL WHERE member_id = ?", (loan['member_id'],))
        
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'Denda lunas.'})

@app.route('/api/sirkulasi/borrow', methods=['POST'])
@api_login_required
def api_borrow():
    data = request.json
    member_id = data.get('member_id')
    book_id = data.get('book_id')
    
    conn = database.get_db_connection()
    eksemplar = conn.execute("SELECT e.*, b.judul FROM eksemplar e JOIN bibliografi b ON e.biblio_id = b.id WHERE e.no_induk = ?", (book_id,)).fetchone()
    
    if not eksemplar:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Buku dengan Barcode tersebut tidak ditemukan'})
        
    eksemplar = dict(eksemplar)
    if eksemplar.get('is_reference_only'):
        conn.close()
        return jsonify({'status': 'error', 'message': 'Buku ini adalah buku Referensi dan TIDAK BOLEH dipinjam.'})
    if eksemplar.get('status_buku') == 'DIPINJAM':
        conn.close()
        return jsonify({'status': 'error', 'message': 'Buku saat ini sedang berstatus dipinjam orang lain.'})
        
    import datetime
    loan_date = datetime.datetime.now()
    due_date = loan_date + datetime.timedelta(days=14)
    
    conn.execute("INSERT INTO sirkulasi (member_id, no_induk, loan_date, due_date) VALUES (?, ?, ?, ?)", (member_id, book_id, loan_date.strftime('%Y-%m-%d %H:%M:%S'), due_date.strftime('%Y-%m-%d %H:%M:%S')))
    conn.execute("UPDATE eksemplar SET status_buku = 'DIPINJAM' WHERE no_induk = ?", (book_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'data': {'buku_judul': eksemplar.get('judul')}})

def calculate_working_days(start_date, end_date, conn):
    import datetime
    try:
        libur_rows = conn.execute("SELECT tanggal FROM hari_libur").fetchall()
        libur_set = set(row[0] for row in libur_rows)
    except:
        libur_set = set()
    
    days = (end_date - start_date).days
    working_days = 0
    for i in range(1, days + 1):
        day = start_date + datetime.timedelta(days=i)
        if day.weekday() < 5 and day.strftime('%Y-%m-%d') not in libur_set:
            working_days += 1
    return working_days


@app.route('/api/sirkulasi/renew', methods=['POST'])
@api_login_required
def api_renew():
    data = request.json
    book_id = data.get('book_id')
    
    conn = database.get_db_connection()
    loan = conn.execute("""
        SELECT s.*, s.member_id as e_member_id, a.tipe_anggota 
        FROM sirkulasi s 
        JOIN eksemplar e ON s.no_induk = e.no_induk 
        LEFT JOIN anggota a ON s.member_id = a.member_id 
        WHERE s.no_induk = ? AND s.return_date IS NULL
    """, (book_id,)).fetchone()
    
    if not loan:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Tidak ada peminjaman aktif untuk buku ini.'})
        
    loan = dict(loan)
    tipe = loan.get('tipe_anggota', 'Reguler')
    if tipe is None:
        tipe = 'Reguler'
        
    # Check max renewals (Reguler = 2, Skripsi = unlimited)
    member = conn.execute("SELECT is_tesis FROM anggota WHERE member_id = ?", (loan['member_id'],)).fetchone()
    is_tesis = member['is_tesis'] if member else 0
    
    if not is_tesis and loan['renewal_count'] >= 1:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Batas maksimal perpanjangan (1 kali) telah tercapai untuk anggota non-tesis/skripsi.'})
        
    import datetime
    # Perpanjang 14 hari dari HARI INI
    new_due_date = datetime.datetime.now() + datetime.timedelta(days=14)
    new_count = loan['renewal_count'] + 1
    
    conn.execute("UPDATE sirkulasi SET due_date = ?, renewal_count = ? WHERE id = ?", (new_due_date.strftime('%Y-%m-%d %H:%M:%S'), new_count, loan['id']))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'Berhasil diperpanjang 14 hari.', 'new_due_date': new_due_date.strftime('%Y-%m-%d')})


@app.route('/api/kiosk_pinjam', methods=['POST'])
def api_kiosk_pinjam():
    data = request.json
    member_id = data.get('member_id')
    no_induk = data.get('no_induk')
    
    if not member_id or not no_induk:
        return jsonify({'status': 'error', 'message': 'Data tidak lengkap.'})
        
    conn = database.get_db_connection()
    member = conn.execute("SELECT * FROM anggota WHERE member_id = ?", (member_id,)).fetchone()
    if not member:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Anggota tidak ditemukan.'})
        
    if member['status'] != 'AKTIF':
        conn.close()
        return jsonify({'status': 'error', 'message': 'Kartu anggota sedang tidak aktif.'})
        
    # Check max loans
    is_tesis = member['is_tesis']
    max_loans = 4 if is_tesis else 2
    
    current_loans = conn.execute("SELECT COUNT(*) FROM sirkulasi WHERE member_id = ? AND return_date IS NULL", (member_id,)).fetchone()[0]
    if current_loans >= max_loans:
        conn.close()
        return jsonify({'status': 'error', 'message': f'Batas pinjaman maksimal tercapai ({max_loans} buku).'})
        
    # Check fines
    fines = conn.execute("SELECT SUM(fine_amount) FROM sirkulasi WHERE member_id = ? AND fine_status = 'BELUM_LUNAS'", (member_id,)).fetchone()[0] or 0
    if fines > 0:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Anda memiliki denda yang belum lunas. Selesaikan denda di petugas terlebih dahulu.'})
        
    # Check if book exists and available
    book = conn.execute("SELECT e.*, b.judul FROM eksemplar e JOIN bibliografi b ON e.biblio_id = b.id WHERE e.no_induk = ?", (no_induk,)).fetchone()
    if not book:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Buku tidak ditemukan di katalog.'})
        
    is_borrowed = conn.execute("SELECT id FROM sirkulasi WHERE no_induk = ? AND return_date IS NULL", (no_induk,)).fetchone()
    if is_borrowed:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Buku ini sedang dipinjam oleh orang lain.'})
        
    # Process loan
    import datetime
    loan_date = datetime.datetime.now()
    due_date = loan_date + datetime.timedelta(days=14)
    
    conn.execute("INSERT INTO sirkulasi (member_id, no_induk, loan_date, due_date) VALUES (?, ?, ?, ?)",
                 (member_id, no_induk, loan_date.strftime('%Y-%m-%d %H:%M:%S'), due_date.strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()
    
    return jsonify({
        'status': 'success',
        'judul': book['judul'],
        'due_date': due_date.strftime('%Y-%m-%d')
    })

@app.route('/api/sirkulasi/return', methods=['POST'])
@api_login_required
def api_return():
    data = request.json
    book_id = data.get('book_id')
    
    conn = database.get_db_connection()
    loan = conn.execute("SELECT s.*, s.member_id as e_member_id, a.nama as anggota_nama, b.judul FROM sirkulasi s JOIN eksemplar e ON s.no_induk = e.no_induk JOIN bibliografi b ON e.biblio_id = b.id LEFT JOIN anggota a ON s.member_id = a.member_id WHERE s.no_induk = ? AND s.return_date IS NULL", (book_id,)).fetchone()
    
    if not loan:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Tidak ada catatan peminjaman aktif untuk buku ini.'})
        
    loan = dict(loan)
    import datetime
    
    return_datetime = datetime.datetime.now()
    due_datetime = datetime.datetime.strptime(loan['due_date'], '%Y-%m-%d %H:%M:%S')
    
    denda = 0
    terlambat_hari = 0
    
    if return_datetime.date() > due_datetime.date():
        terlambat_hari = calculate_working_days(due_datetime.date(), return_datetime.date(), conn)
        denda = terlambat_hari * 500
        
    conn.execute("UPDATE sirkulasi SET return_date = ?, fine_amount = ?, fine_status = ? WHERE id = ?", (return_datetime.strftime('%Y-%m-%d %H:%M:%S'), denda, 'BELUM_LUNAS' if denda > 0 else 'LUNAS', loan['id']))
    conn.execute("UPDATE eksemplar SET status_buku = 'TERSEDIA' WHERE no_induk = ?", (book_id,))
    
    if denda > 0:
        suspend_until = return_datetime.date() + datetime.timedelta(days=1)
        conn.execute("UPDATE anggota SET status = 'DIBLOKIR', suspended_until = ? WHERE member_id = ?", (suspend_until.strftime('%Y-%m-%d'), loan['member_id']))
        
    conn.commit()
    conn.close()
    
    return jsonify({
        'status': 'success',
        'data': {
            'buku_judul': loan.get('judul'),
            'anggota_nama': loan.get('anggota_nama'),
            'denda': denda,
            'terlambat_hari': terlambat_hari
        }
    })


@app.route('/api/buku/missing_covers', methods=['GET'])
def api_missing_covers():
    conn = database.get_db_connection()
    # Get up to 100 books that lack both ISBN and image
    cursor = conn.execute("SELECT id, judul, pengarang FROM bibliografi WHERE (isbn IS NULL OR isbn = '') AND (image IS NULL OR image = '') LIMIT 50")
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

@app.route('/api/buku/save_cover', methods=['POST'])
def api_save_cover():
    data = request.json
    biblio_id = data.get('id')
    url = data.get('url')
    if biblio_id and url:
        conn = database.get_db_connection()
        conn.execute("UPDATE bibliografi SET image = ? WHERE id = ?", (url, biblio_id))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'})


# ==========================================
# OPAC & PUBLIC APIs
# ==========================================

@app.route('/api/opac/search', methods=['GET'])
def api_opac_search():
    search = request.args.get('q', '').strip()
    if not search:
        return jsonify([])
        
    conn = database.get_db_connection()
    
    # Track zero-result queries if they yield nothing (handled below)
    query = """
        SELECT b.id, b.judul, b.pengarang, b.penerbit, b.tahun_terbit, b.klasifikasi, b.image, b.isbn,
               COUNT(e.no_induk) as total_eksemplar,
               SUM(CASE WHEN (e.status_ketersediaan = 'Tersedia' AND (e.status_buku IS NULL OR e.status_buku != 'DIPINJAM')) THEN 1 ELSE 0 END) as tersedia
        FROM bibliografi b
        LEFT JOIN eksemplar e ON b.id = e.biblio_id
        WHERE b.judul LIKE ? OR b.pengarang LIKE ? OR b.penerbit LIKE ? OR b.klasifikasi LIKE ?
        GROUP BY b.id
        ORDER BY b.id DESC
        LIMIT 50
    """
    cursor = conn.execute(query, (f'%{search}%', f'%{search}%', f'%{search}%', f'%{search}%'))
    results = [dict(row) for row in cursor.fetchall()]
    
    import re
    for row in results:
        # Resolve Cover URL
        if row.get('image'):
            if row['image'] == 'NOT_FOUND':
                row['cover_url'] = None
            elif row['image'].startswith('http'):
                row['cover_url'] = row['image']
            else:
                row['cover_url'] = f"/static/uploads/{row['image']}"
        elif row.get('isbn'):
            raw_isbn = str(row['isbn']).split(',')[0].split(' ')[0].upper()
            cleaned = re.sub(r'[^0-9X]', '', raw_isbn)
            if cleaned:
                row['cover_url'] = f"https://books.google.com/books/content?vid=ISBN{cleaned}&printsec=frontcover&img=1&zoom=1"
            else:
                row['cover_url'] = None
        else:
            row['cover_url'] = None
            
        # Resolve Wayfinding (Location)
        klas = str(row.get('klasifikasi', ''))
        lokasi = "Lantai 1 ? Rak Umum"
        if klas.startswith('1'): lokasi = "Lantai 1 ? Rak Filsafat & Psikologi (100)"
        elif klas.startswith('2'): lokasi = "Lantai 1 ? Rak Agama & Teologi (200)"
        elif klas.startswith('3'): lokasi = "Lantai 1 ? Rak Ilmu Sosial (300)"
        elif klas.startswith('4'): lokasi = "Lantai 2 ? Rak Bahasa (400)"
        elif klas.startswith('5'): lokasi = "Lantai 2 ? Rak Sains & Matematika (500)"
        elif klas.startswith('6'): lokasi = "Lantai 2 ? Rak Teknologi (600)"
        elif klas.startswith('7'): lokasi = "Lantai 2 ? Rak Seni & Rekreasi (700)"
        elif klas.startswith('8'): lokasi = "Lantai 3 ? Rak Sastra (800)"
        elif klas.startswith('9'): lokasi = "Lantai 3 ? Rak Sejarah & Geografi (900)"
        row['lokasi_rak'] = lokasi

    # Zero-Result Hook Logging
    if len(results) == 0 and len(search) > 3:
        try:
            conn.execute("""
                INSERT INTO pencarian_gagal (keyword, jumlah_pencarian)
                VALUES (?, 1)
                ON CONFLICT(keyword) DO UPDATE SET 
                jumlah_pencarian = jumlah_pencarian + 1,
                update_terakhir = CURRENT_TIMESTAMP
            """, (search.lower(),))
            conn.commit()
        except:
            pass
            
    conn.close()
    return jsonify(results)

@app.route('/api/opac/request', methods=['POST'])
def api_opac_request():
    data = request.json
    judul = data.get('judul')
    pengarang = data.get('pengarang', '')
    catatan = data.get('catatan', '')
    
    if not judul:
        return jsonify({'status': 'error', 'message': 'Judul/Topik wajib diisi'}), 400
        
    conn = database.get_db_connection()
    conn.execute(
        "INSERT INTO usulan_buku (judul_topik, pengarang, catatan) VALUES (?, ?, ?)",
        (judul, pengarang, catatan)
    )
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/api/opac/reserve', methods=['POST'])
def api_opac_reserve():
    data = request.json
    biblio_id = data.get('biblio_id')
    nim = data.get('nim')
    
    if not biblio_id or not nim:
        return jsonify({'status': 'error', 'message': 'NIM dan ID Buku wajib diisi'}), 400
        
    conn = database.get_db_connection()
    
    # Check if already reserved
    existing = conn.execute("SELECT id FROM reservasi WHERE biblio_id = ? AND nim_pemustaka = ? AND status = 'Aktif'", (biblio_id, nim)).fetchone()
    if existing:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Anda sudah mereservasi buku ini dan sedang dalam antrean.'}), 400
        
    conn.execute(
        "INSERT INTO reservasi (biblio_id, nim_pemustaka) VALUES (?, ?)",
        (biblio_id, nim)
    )
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})



@app.route('/kelola_sampul')
@login_required
def kelola_sampul():
    return render_template('kelola_sampul.html')

@app.route('/api/sampul_kosong', methods=['GET'])
@api_login_required
def api_sampul_kosong():
    search = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    per_page = 15
    offset = (page - 1) * per_page
    
    conn = database.get_db_connection()
    query = '''
        SELECT id, judul, pengarang, penerbit, tahun_terbit, isbn
        FROM bibliografi
        WHERE (image IS NULL OR image = '' OR image = 'NOT_FOUND' OR image = 'RATE_LIMIT')
    '''
    params = []
    
    if search:
        query += ' AND (judul LIKE ? OR pengarang LIKE ? OR isbn LIKE ?)'
        params.extend(['%'+search+'%', '%'+search+'%', '%'+search+'%'])
        
    count_query = query.replace('SELECT id, judul, pengarang, penerbit, tahun_terbit, isbn', 'SELECT COUNT(*) as total')
    cursor = conn.execute(count_query, params)
    total = cursor.fetchone()['total']
    
    query += ' ORDER BY id DESC LIMIT ? OFFSET ?'
    params.extend([per_page, offset])
    
    cursor = conn.execute(query, params)
    books = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        'status': 'success',
        'data': books,
        'total': total,
        'page': page,
        'total_pages': (total + per_page - 1) // per_page
    })

@app.route('/api/sampul/update', methods=['POST'])
@api_login_required
def api_sampul_update():
    data = request.json
    biblio_id = data.get('id')
    image_url = data.get('image_url')
    
    if not biblio_id or not image_url:
        return jsonify({'status': 'error', 'message': 'Data tidak lengkap'}), 400
        
    conn = database.get_db_connection()
    conn.execute('UPDATE bibliografi SET image = ? WHERE id = ?', (image_url, biblio_id))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success'})



@app.route('/api/opac/discover_cover', methods=['POST'])
def api_opac_discover_cover():
    data = request.json
    biblio_id = data.get('id')
    image_url = data.get('image_url')
    
    if not biblio_id or not image_url or not str(image_url).startswith('http'):
        return jsonify({'status': 'error'}), 400
        
    try:
        conn = database.get_db_connection()
        conn.execute('''
            UPDATE bibliografi 
            SET image = ? 
            WHERE id = ? AND (image IS NULL OR image = '' OR image = 'NOT_FOUND' OR image = 'RATE_LIMIT')
        ''', (image_url, biblio_id))
        conn.commit()
        conn.close()
    except:
        pass
    

        
    return jsonify({'status': 'success'})



import threading
import json
import urllib.request
import urllib.parse

# Startup Migrations
try:
    _conn = database.get_db_connection()
    _conn.execute("ALTER TABLE anggota ADD COLUMN is_tesis INTEGER DEFAULT 0")
    _conn.commit()
    _conn.close()
    print("Migrasi: Kolom is_tesis berhasil ditambahkan ke tabel anggota.")
except Exception as e:
    pass # Kemungkinan kolom sudah ada

try:
    _conn = database.get_db_connection()
    _conn.execute("ALTER TABLE anggota ADD COLUMN tanggal_input TEXT")
    _conn.commit()
    _conn.close()
except:
    pass

import time
import os

ROBOT_STATE_FILE = 'robot_state.json'

def get_robot_state():
    try:
        with open(ROBOT_STATE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"is_running": False, "progress": 0, "total": 0, "current_book": "", "results": [], "error": ""}

def save_robot_state(state):
    with open(ROBOT_STATE_FILE, 'w') as f:
        json.dump(state, f)

def robot_worker(limit=50):
    state = {"is_running": True, "progress": 0, "total": limit, "current_book": "Memulai...", "results": [], "error": ""}
    save_robot_state(state)
    
    conn = database.get_db_connection()
    cursor = conn.execute("SELECT id, judul, pengarang FROM bibliografi WHERE image IS NULL OR image = '' OR image = 'NOT_FOUND' OR image = 'RATE_LIMIT' LIMIT ?", (limit,))
    books = cursor.fetchall()
    
    if not books:
        state["is_running"] = False
        state["current_book"] = "Selesai"
        state["error"] = "Luar biasa! Tidak ada lagi buku yang membutuhkan sampul."
        save_robot_state(state)
        conn.close()
        return
        
    state["total"] = len(books)
    
    for row in books:
        current_state = get_robot_state()
        if not current_state.get("is_running"):
            break # manual stop
            
        biblio_id, judul, pengarang = row['id'], row['judul'], row['pengarang']
        state["current_book"] = f"{judul} - {pengarang}"
        save_robot_state(state)
        
        query = (judul or "") + " " + (pengarang or "")
        image_url = 'NOT_FOUND'
        
        try:
            url = "https://www.googleapis.com/books/v1/volumes?q=" + urllib.parse.quote(query)
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                if 'items' in data and len(data['items']) > 0:
                    img = data['items'][0]['volumeInfo'].get('imageLinks', {}).get('thumbnail')
                    if img:
                        image_url = img.replace('http:', 'https:')
        except urllib.error.HTTPError as e:
            if e.code == 429:
                image_url = 'RATE_LIMIT'
        except Exception:
            pass
            
        conn.execute("UPDATE bibliografi SET image = ? WHERE id = ?", (image_url, biblio_id))
        conn.commit()
        
        status_text = "Ditemukan" if image_url.startswith('http') else ("Limit Google" if image_url == 'RATE_LIMIT' else "Kosong")
        
        # Add to beginning of results so newest is at top
        state["results"].insert(0, {
            "judul": judul,
            "status": status_text,
            "image_url": image_url if image_url.startswith('http') else None
        })
        state["progress"] += 1
        save_robot_state(state)
        
        if image_url == 'RATE_LIMIT':
            state["error"] = "Terhenti otomatis karena Google mendeteksi terlalu banyak permintaan. Silakan coba lagi nanti."
            break
            
        time.sleep(2.5) # Sleep 2.5 seconds to be safe
        
    state["is_running"] = False
    state["current_book"] = "Selesai"
    save_robot_state(state)
    conn.close()

@app.route('/api/robot/start', methods=['POST'])
@api_login_required
def api_robot_start():
    state = get_robot_state()
    if state.get("is_running"):
        return jsonify({'status': 'error', 'message': 'Robot sedang berjalan!'})
        
    limit = request.json.get('limit', 50)
    thread = threading.Thread(target=robot_worker, args=(limit,))
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'success'})

@app.route('/api/robot/stop', methods=['POST'])
@api_login_required
def api_robot_stop():
    state = get_robot_state()
    state["is_running"] = False
    state["error"] = "Dihentikan manual oleh admin."
    save_robot_state(state)
    return jsonify({'status': 'success'})

@app.route('/api/robot/status', methods=['GET'])
@api_login_required
def api_robot_status():
    return jsonify(get_robot_state())



@app.route('/sirkulasi/cetak_struk/<member_id>')
def cetak_struk(member_id):
    conn = database.get_db_connection()
    member = conn.execute("SELECT * FROM anggota WHERE member_id = ?", (member_id,)).fetchone()
    if not member:
        conn.close()
        return "Anggota tidak ditemukan", 404
        
    # Get active loans
    loans = conn.execute("SELECT s.*, b.judul FROM sirkulasi s JOIN eksemplar e ON s.no_induk = e.no_induk JOIN bibliografi b ON e.biblio_id = b.id WHERE s.member_id = ? AND s.return_date IS NULL ORDER BY s.loan_date DESC", (member_id,)).fetchall()
    conn.close()
    
    return render_template('cetak_struk.html', member=dict(member), loans=[dict(l) for l in loans])



@app.route('/cek_pinjaman/<member_id>')
def cek_pinjaman(member_id):
    conn = database.get_db_connection()
    member = conn.execute("SELECT * FROM anggota WHERE member_id = ?", (member_id,)).fetchone()
    if not member:
        conn.close()
        return "Anggota tidak ditemukan", 404
        
    loans = conn.execute("SELECT s.*, b.judul, b.image, b.pengarang FROM sirkulasi s JOIN eksemplar e ON s.no_induk = e.no_induk JOIN bibliografi b ON e.biblio_id = b.id WHERE s.member_id = ? AND s.return_date IS NULL ORDER BY s.due_date ASC", (member_id,)).fetchall()
    
    # Check fines
    fines = conn.execute("SELECT SUM(fine_amount) FROM sirkulasi WHERE member_id = ? AND fine_status = 'BELUM_LUNAS'", (member_id,)).fetchone()[0] or 0
    
    conn.close()
    return render_template('cek_pinjaman.html', member=dict(member), loans=[dict(l) for l in loans], total_denda=fines)




@app.route('/self_checkout/<member_id>')
def self_checkout(member_id):
    conn = database.get_db_connection()
    member = conn.execute("SELECT * FROM anggota WHERE member_id = ?", (member_id,)).fetchone()
    if not member:
        conn.close()
        return "Anggota tidak ditemukan", 404
        
    loans = conn.execute("SELECT s.*, b.judul, b.image, b.pengarang FROM sirkulasi s JOIN eksemplar e ON s.no_induk = e.no_induk JOIN bibliografi b ON e.biblio_id = b.id WHERE s.member_id = ? AND s.return_date IS NULL ORDER BY s.due_date ASC", (member_id,)).fetchall()
    
    # Check fines
    fines = conn.execute("SELECT SUM(fine_amount) FROM sirkulasi WHERE member_id = ? AND fine_status = 'BELUM_LUNAS'", (member_id,)).fetchone()[0] or 0
    
    conn.close()
    return render_template('self_checkout.html', member=dict(member), loans=[dict(l) for l in loans], total_denda=fines)

@app.route('/kiosk_sirkulasi')
def kiosk_sirkulasi():
    return render_template('kiosk_sirkulasi.html')



@app.route('/sirkulasi/cetak_struk_kembali/<member_id>')
@login_required
def cetak_struk_kembali(member_id):
    conn = database.get_db_connection()
    member = conn.execute("SELECT * FROM anggota WHERE member_id = ?", (member_id,)).fetchone()
    if not member:
        conn.close()
        return "Anggota tidak ditemukan", 404
        
    # Ambil buku yang dikembalikan HARI INI oleh member ini
    returns = conn.execute("SELECT s.*, b.judul FROM sirkulasi s JOIN eksemplar e ON s.no_induk = e.no_induk JOIN bibliografi b ON e.biblio_id = b.id WHERE s.member_id = ? AND s.return_date IS NOT NULL AND date(s.return_date) = date('now', 'localtime') ORDER BY s.return_date DESC", (member_id,)).fetchall()
    conn.close()
    
    return render_template('cetak_struk_kembali.html', member=dict(member), returns=[dict(r) for r in returns])



@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    conn = database.get_db_connection()
    if request.method == 'POST':
        # Simpan pengaturan
        token = request.form.get('telegram_token', '').strip()
        chat_id = request.form.get('telegram_chat_id', '').strip()
        gemini_key = request.form.get('gemini_api_key', '').strip()
        
        conn.execute("INSERT OR REPLACE INTO pengaturan_sistem (kunci, nilai) VALUES ('TELEGRAM_BOT_TOKEN', ?)", (token,))
        conn.execute("INSERT OR REPLACE INTO pengaturan_sistem (kunci, nilai) VALUES ('TELEGRAM_CHAT_ID', ?)", (chat_id,))
        conn.execute("INSERT OR REPLACE INTO pengaturan_sistem (kunci, nilai) VALUES ('GEMINI_API_KEY', ?)", (gemini_key,))
        conn.commit()
        flash("Pengaturan berhasil disimpan!", "success")
        return redirect(url_for('settings'))
        
    # Ambil pengaturan saat ini
    config = {}
    rows = conn.execute("SELECT kunci, nilai FROM pengaturan_sistem").fetchall()
    for row in rows:
        config[row['kunci']] = row['nilai']
        
    conn.close()
    return render_template('settings.html', config=config)

@app.route('/api/test_backup', methods=['POST'])
@login_required
def test_backup():
    import telegram_backup
    import traceback
    try:
        success, message = telegram_backup.run_backup(manual=True)
        return jsonify({
            'status': 'success' if success else 'error',
            'message': message
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'trace': traceback.format_exc()
        })



import threading
import time
import datetime
import telegram_backup

def daily_backup_job():
    while True:
        now = datetime.datetime.now()
        # Hitung waktu sampai jam 00:00 berikutnya
        tomorrow = now + datetime.timedelta(days=1)
        target = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 1, 0)
        sleep_seconds = (target - now).total_seconds()
        time.sleep(sleep_seconds)
        
        try:
            telegram_backup.run_backup(manual=False)
        except Exception as e:
            print("Auto-backup failed:", e)

# Jalankan scheduler di background thread
backup_thread = threading.Thread(target=daily_backup_job, daemon=True)
backup_thread.start()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

@app.route('/api/debug/db_path', methods=['GET'])
def api_debug_db():
    import os
    import database
    return jsonify({
        'cwd': os.getcwd(),
        'db_path_relative': database.DB_NAME,
        'db_path_absolute': os.path.abspath(database.DB_NAME),
        'db_exists': os.path.exists(os.path.abspath(database.DB_NAME))
    })

@app.route('/api/debug/tables', methods=['GET'])
def api_debug_tables():
    import database
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    eksemplar_count = 0
    sirkulasi_count = 0
    if 'eksemplar' in tables:
        eksemplar_count = conn.execute("SELECT COUNT(*) FROM eksemplar").fetchone()[0]
    if 'sirkulasi' in tables:
        sirkulasi_count = conn.execute("SELECT COUNT(*) FROM sirkulasi").fetchone()[0]
        
    conn.close()
    return jsonify({
        'tables': tables,
        'eksemplar_count': eksemplar_count,
        'sirkulasi_count': sirkulasi_count
    })

@app.route('/api/debug/force_migrate', methods=['GET'])
def api_force_migrate():
    import database
    import traceback
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        # 1. Create bibliografi
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS bibliografi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            gmd TEXT DEFAULT 'Text',
            edisi TEXT,
            isbn TEXT,
            penerbit TEXT,
            tahun_terbit TEXT,
            deskripsi_fisik TEXT,
            judul_seri TEXT,
            klasifikasi TEXT,
            cutter TEXT,
            huruf_judul TEXT,
            bahasa TEXT DEFAULT 'Indonesia',
            tempat_terbit TEXT,
            pengarang TEXT,
            subjek TEXT,
            image TEXT
        )
        """)

        # 2. Create eksemplar
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS eksemplar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            biblio_id INTEGER NOT NULL,
            no_induk TEXT UNIQUE NOT NULL,
            status_buku TEXT DEFAULT 'BELI',
            lokasi TEXT DEFAULT 'IMAVI',
            tgl_terima TEXT,
            copy_ke INTEGER DEFAULT 1,
            catatan TEXT,
            status_ketersediaan TEXT DEFAULT 'Tersedia',
            FOREIGN KEY (biblio_id) REFERENCES bibliografi(id)
        )
        """)
        
        # 3. Migrate data if empty
        msg = "Tables created."
        # Selalu reset dan migrasi ulang untuk memperbaiki duplikat
        cursor.execute("DELETE FROM eksemplar")
        cursor.execute("DELETE FROM bibliografi")
        
        cursor.execute("SELECT * FROM buku")
        buku_rows = cursor.fetchall()
        cursor.execute("PRAGMA table_info(buku)")
        columns = [col[1] for col in cursor.fetchall()]
        
        biblio_map = {} # (judul, pengarang, penerbit) -> biblio_id
        
        migrated_count = 0
        for row in buku_rows:
            row_dict = dict(zip(columns, row))
            key = (row_dict.get('judul', ''), row_dict.get('pengarang', ''), row_dict.get('penerbit', ''))
            
            if key not in biblio_map:
                cursor.execute("""
                    INSERT INTO bibliografi (
                        judul, gmd, edisi, isbn, penerbit, tahun_terbit, deskripsi_fisik, 
                        judul_seri, klasifikasi, cutter, huruf_judul, bahasa, tempat_terbit, 
                        pengarang, subjek
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row_dict.get('judul'), row_dict.get('gmd'), row_dict.get('edisi'), 
                    row_dict.get('isbn'), row_dict.get('penerbit'), row_dict.get('tahun_terbit'), 
                    row_dict.get('deskripsi_fisik'), row_dict.get('judul_seri'), 
                    row_dict.get('klasifikasi'), row_dict.get('cutter'), row_dict.get('huruf_judul'), 
                    row_dict.get('bahasa'), row_dict.get('tempat_terbit'), row_dict.get('pengarang'), 
                    row_dict.get('subjek')
                ))
                biblio_map[key] = cursor.lastrowid
            
            biblio_id = biblio_map[key]
            
            cursor.execute("""
                INSERT INTO eksemplar (
                    biblio_id, no_induk, status_buku, lokasi, tgl_terima, copy_ke, catatan
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                biblio_id, row_dict.get('no_induk'), row_dict.get('status_buku'), 
                row_dict.get('lokasi'), row_dict.get('tgl_terima'), row_dict.get('copy_ke'), 
                row_dict.get('catatan')
            ))
            migrated_count += 1
        msg += f" Migrated {migrated_count} copies into {len(biblio_map)} titles."
        
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': msg})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e), 'trace': traceback.format_exc()})

@app.route('/api/ddc/search', methods=['GET'])
@api_login_required
def api_ddc_search():
    keyword = request.args.get('q', '').lower()
    import json
    try:
        with open('ddc_kamus.json', 'r') as f:
            ddc_dict = json.load(f)
    except:
        ddc_dict = {}
        
    results = []
    
    # Clean keywords (ignore short words)
    ignore_words = ['pengantar', 'buku', 'panduan', 'dasar', 'teori', 'ilmu', 'dan', 'yang']
    keywords = [w for w in keyword.split() if w not in ignore_words and len(w) > 2]
    
    # If no keywords left, just search the original keyword
    if not keywords:
        keywords = [keyword]
        
    for code, desc in ddc_dict.items():
        # exact match
        if keyword in desc.lower():
            results.append({'kode': code, 'deskripsi': desc})
            continue
            
        # keyword match
        for kw in keywords:
            if kw in desc.lower():
                results.append({'kode': code, 'deskripsi': desc})
                break
                
    return jsonify(results)


@app.route('/api/bibliografi/search', methods=['GET'])
@api_login_required
def api_biblio_search():
    keyword = request.args.get('q', '')
    conn = database.get_db_connection()
    # Search by title or author
    cursor = conn.execute("SELECT * FROM bibliografi WHERE judul LIKE ? OR pengarang LIKE ? LIMIT 10", (f'%{keyword}%', f'%{keyword}%'))
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

@app.route('/api/buku/input_batch', methods=['POST'])
@api_login_required
def api_input_batch():
    from werkzeug.utils import secure_filename
    import os
    
    # Check if request is JSON (old behavior) or form data (new behavior with image)
    if request.is_json:
        data = request.json
    else:
        data = request.form

    biblio_id = data.get('biblio_id')
    jumlah_eksemplar = int(data.get('jumlah', 1))
    
    conn = database.get_db_connection()
    
    # Handle image upload
    image_filename = None
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            upload_dir = os.path.join(app.root_path, 'static', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            file.save(os.path.join(upload_dir, filename))
            image_filename = filename
    
    # 1. Handle Bibliografi
    if not biblio_id:
        # Create new bibliografi
        cursor = conn.execute("""
            INSERT INTO bibliografi (
                judul, pengarang, penerbit, isbn, klasifikasi, tempat_terbit, 
                tahun_terbit, edisi, bahasa, gmd, deskripsi_fisik, judul_seri, 
                cutter, huruf_judul, subjek, image
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get('judul'), data.get('pengarang'), data.get('penerbit'), data.get('isbn'),
            data.get('klasifikasi'), data.get('tempat_terbit'), data.get('tahun_terbit'),
            data.get('edisi'), data.get('bahasa', 'Indonesia'),
            data.get('gmd', 'Text'), data.get('deskripsi_fisik'), data.get('judul_seri'),
            data.get('cutter'), data.get('huruf_judul'), data.get('subjek'), image_filename
        ))
        biblio_id = cursor.lastrowid
    else:
        # Update existing bibliografi
        update_query = """
            UPDATE bibliografi SET 
                judul=?, pengarang=?, penerbit=?, isbn=?, klasifikasi=?, tempat_terbit=?, 
                tahun_terbit=?, edisi=?, bahasa=?, gmd=?, deskripsi_fisik=?, judul_seri=?, 
                cutter=?, huruf_judul=?, subjek=?
            WHERE id=?
        """
        conn.execute(update_query, (
            data.get('judul'), data.get('pengarang'), data.get('penerbit'), data.get('isbn'),
            data.get('klasifikasi'), data.get('tempat_terbit'), data.get('tahun_terbit'),
            data.get('edisi'), data.get('bahasa', 'Indonesia'),
            data.get('gmd', 'Text'), data.get('deskripsi_fisik'), data.get('judul_seri'),
            data.get('cutter'), data.get('huruf_judul'), data.get('subjek'), biblio_id
        ))
        if image_filename:
            conn.execute("UPDATE bibliografi SET image = ? WHERE id = ?", (image_filename, biblio_id))
        
        # Also update status_buku in all eksemplar
        if data.get('status_buku'):
            conn.execute("UPDATE eksemplar SET status_buku = ? WHERE biblio_id = ?", (data.get('status_buku'), biblio_id))

    
    if jumlah_eksemplar > 0:

        import datetime
        current_year = datetime.datetime.now().strftime('%y') # e.g. '26'
    
        # Find max sequence for this year in eksemplar
        max_seq_row = conn.execute("SELECT no_induk FROM eksemplar WHERE no_induk LIKE ? ORDER BY no_induk DESC LIMIT 1", (f'%/{current_year}',)).fetchone()
    
        start_num = 1
        if max_seq_row:
            try:
                start_num = int(max_seq_row[0].split('/')[0]) + 1
            except:
                start_num = 1
            
        generated_barcodes = []
        for i in range(jumlah_eksemplar):
            new_barcode = f"{(start_num + i):04d}/{current_year}"
            conn.execute("""
                INSERT INTO eksemplar (biblio_id, no_induk, status_buku, lokasi, tgl_terima, copy_ke)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                biblio_id, new_barcode, data.get('status_buku', 'BELI'), data.get('lokasi', 'IMAVI'),
                datetime.datetime.now().strftime('%Y-%m-%d'), (i+1)
            ))
            generated_barcodes.append(new_barcode)
        
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'status': 'success', 
        'message': f'Berhasil menyimpan bibliografi dan {jumlah_eksemplar} eksemplar.',
        'barcodes': generated_barcodes
    })


@app.route('/api/koleksi/list', methods=['GET'])
@api_login_required
def api_koleksi_list():
    import traceback
    try:
        search = request.args.get('search', '')
        page = int(request.args.get('page', 1))
        cover_status = request.args.get('cover_status', 'all')
        per_page = 20
        offset = (page - 1) * per_page
        
        conn = database.get_db_connection()
        
        where_clause = "(b.judul LIKE ? OR b.pengarang LIKE ? OR b.klasifikasi LIKE ?)"
        params = [f'%{search}%', f'%{search}%', f'%{search}%']
        
        if cover_status == 'has_cover':
            where_clause += " AND ((b.image IS NOT NULL AND b.image != '' AND b.image != 'NOT_FOUND') OR (b.isbn IS NOT NULL AND b.isbn != ''))"
        elif cover_status == 'no_cover':
            where_clause += " AND (b.isbn IS NULL OR b.isbn = '') AND (b.image IS NULL OR b.image = '' OR b.image = 'NOT_FOUND')"
            
        query = f"""
            SELECT b.*, COUNT(e.no_induk) as jumlah_eksemplar
            FROM bibliografi b
            LEFT JOIN eksemplar e ON b.id = e.biblio_id
            WHERE {where_clause}
            GROUP BY b.id
            ORDER BY b.id DESC
            LIMIT ? OFFSET ?
        """
        cursor = conn.execute(query, tuple(params + [per_page, offset]))
        results = [dict(row) for row in cursor.fetchall()]
        
        import re
        for row in results:
            if row.get('image'):
                if row['image'] == 'NOT_FOUND':
                    row['cover_url'] = None
                elif row['image'].startswith('http'):
                    row['cover_url'] = row['image']
                else:
                    row['cover_url'] = f"/static/uploads/{row['image']}"
            elif row.get('isbn'):
                raw_isbn = str(row['isbn']).split(',')[0].split(' ')[0].upper()
                cleaned = re.sub(r'[^0-9X]', '', raw_isbn)
                if cleaned:
                    row['cover_url'] = f"https://books.google.com/books/content?vid=ISBN{cleaned}&printsec=frontcover&img=1&zoom=1"
                else:
                    row['cover_url'] = None
            else:
                row['cover_url'] = None
        
        total_query = f"SELECT COUNT(*) FROM bibliografi b WHERE {where_clause}"
        total = conn.execute(total_query, tuple(params)).fetchone()[0]
        conn.close()
        return jsonify({
            'data': results,
            'total': total,
            'page': page,
            'total_pages': (total // per_page) + (1 if total % per_page > 0 else 0)
        })
    except Exception as e:
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500


@app.route('/api/koleksi/eksemplar/<int:biblio_id>', methods=['GET'])
@api_login_required
def api_koleksi_eksemplar(biblio_id):
    conn = database.get_db_connection()
    cursor = conn.execute("SELECT no_induk, status_ketersediaan, status_buku, lokasi, tgl_terima FROM eksemplar WHERE biblio_id = ? ORDER BY no_induk", (biblio_id,))
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

@app.route('/api/debug/koleksi', methods=['GET'])
def api_debug_koleksi():
    import traceback
    import database
    try:
        conn = database.get_db_connection()
        query = """
            SELECT b.*, COUNT(e.no_induk) as jumlah_eksemplar
            FROM bibliografi b
            LEFT JOIN eksemplar e ON b.id = e.biblio_id
            WHERE b.judul LIKE ?
            GROUP BY b.id
            ORDER BY b.id DESC
            LIMIT 10
        """
        cursor = conn.execute(query, ('%%',))
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify({'status': 'success', 'data': results})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e), 'trace': traceback.format_exc()})

@app.route('/api/debug/files', methods=['GET'])
def api_debug_files():
    import os
    import database
    
    files_found = []
    
    paths_to_check = [
        '/root/st_jerome_web/katalog.db',
        '/root/katalog.db',
        os.path.join(os.getcwd(), 'katalog.db'),
        os.path.abspath('katalog.db'),
        database.DB_NAME,
        os.path.abspath(database.DB_NAME)
    ]
    
    for p in paths_to_check:
        try:
            if os.path.exists(p):
                size = os.path.getsize(p)
                mtime = os.path.getmtime(p)
                # check if it has bibliografi
                import sqlite3
                conn = sqlite3.connect(p)
                has_bib = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bibliografi'").fetchone() is not None
                conn.close()
                files_found.append({'path': p, 'size': size, 'mtime': mtime, 'has_bibliografi': has_bib})
            else:
                files_found.append({'path': p, 'exists': False})
        except Exception as e:
            files_found.append({'path': p, 'error': str(e)})
            
    return jsonify(files_found)

@app.route('/api/bibliografi/<int:id>', methods=['DELETE'])
@api_login_required
def api_delete_biblio(id):
    import database
    conn = database.get_db_connection()
    # Delete eksemplar first
    conn.execute("DELETE FROM eksemplar WHERE biblio_id = ?", (id,))
    # Delete bibliografi
    conn.execute("DELETE FROM bibliografi WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/api/eksemplar/<path:no_induk>', methods=['DELETE'])
@api_login_required
def api_delete_eksemplar(no_induk):
    import database
    conn = database.get_db_connection()
    conn.execute("DELETE FROM eksemplar WHERE no_induk = ?", (no_induk,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/api/bibliografi/get/<int:id>', methods=['GET'])
@api_login_required
def api_get_biblio(id):
    import database
    conn = database.get_db_connection()
    row = conn.execute("SELECT * FROM bibliografi WHERE id = ?", (id,)).fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    return jsonify({}), 404


import requests
import json

@app.route('/api/wa_webhook', methods=['POST'])
def api_wa_webhook():
    data = request.json
    if not data:
        return jsonify({'status': 'error'})
        
    sender = data.get('from', '')
    message = data.get('body', '')
    name = data.get('sender_name', 'Pengguna')
    
    conn = database.get_db_connection()
    config = conn.execute("SELECT nilai FROM pengaturan_sistem WHERE kunci = 'GEMINI_API_KEY'").fetchone()
    api_key = config['nilai'] if config else None
    
    if not api_key:
        conn.close()
        return jsonify({'reply': 'Mohon maaf, sistem AI perpustakaan saat ini sedang dinonaktifkan (API Key belum diisi oleh Admin).'})
        
    # Ambil sedikit data buku untuk konteks (5 buku terbaru)
    buku = conn.execute("SELECT judul, pengarang, lokasi, status_buku FROM buku LIMIT 10").fetchall()
    buku_context = "\n".join([f"- {b['judul']} (Oleh: {b['pengarang']}) - Lokasi: {b['lokasi']} [{b['status_buku']}]" for b in buku])
    conn.close()
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        system_prompt = f"""Anda adalah St. Jerome Library Assistant, seorang asisten virtual ramah untuk Perpustakaan St. Jerome (Institutum Theologicum Ioannis Mariae Vianney).
        Anda sedang berbicara dengan {name}. Jawab pertanyaan dengan sopan, ramah, dan ringkas (karena ini pesan WhatsApp).
        
        Informasi Perpustakaan:
        - Buka: Senin - Jumat (08:00 - 16:00).
        - Aturan pinjam: Reguler maksimal 2 buku (14 hari). Mahasiswa Tesis/Skripsi maksimal 4 buku (perpanjangan tanpa batas).
        
        Sebagian katalog buku (sebagai contoh jika ditanya):
        {buku_context}
        
        Jika ditanya buku yang tidak ada di atas, katakan untuk datang langsung mengecek OPAC (Katalog Online) perpustakaan.
        """
        
        response = model.generate_content([system_prompt, message])
        reply_text = response.text
        
    except ImportError:
        reply_text = "Sistem AI sedang offline. Admin belum menginstall modul google-generativeai di server."
    except Exception as e:
        reply_text = f"Maaf, saya sedang mengalami gangguan sistem. (Error: {str(e)})"
        
    return jsonify({'reply': reply_text})


@app.route('/wa_broadcast')
@login_required
def wa_broadcast():
    conn = database.get_db_connection()
    total = conn.execute("SELECT COUNT(*) FROM anggota WHERE status = 'AKTIF'").fetchone()[0]
    conn.close()
    return render_template('wa_broadcast.html', total_anggota=total)

import requests

@app.route('/api/wa_broadcast', methods=['POST'])
@api_login_required
def api_wa_broadcast():
    data = request.json
    target = data.get('target')
    msg_template = data.get('message')
    
    if not msg_template:
        return jsonify({'status': 'error', 'message': 'Pesan kosong'})
        
    conn = database.get_db_connection()
    
    query = "SELECT nama, telepon FROM anggota WHERE status = 'AKTIF' AND telepon IS NOT NULL AND telepon != ''"
    if target == 'tesis':
        query += " AND is_tesis = 1"
    elif target == 'reguler':
        query += " AND is_tesis = 0"
        
    members = conn.execute(query).fetchall()
    conn.close()
    
    if not members:
        return jsonify({'status': 'error', 'message': 'Tidak ada anggota yang memenuhi kriteria atau memiliki nomor WA.'})
        
    success_count = 0
    import threading
    
    def send_broadcast_background(members_list, template):
        for m in members_list:
            final_msg = template.replace('[NAMA]', m['nama'])
            try:
                requests.post('http://127.0.0.1:3000/api/send_message', json={
                    'number': m['telepon'],
                    'message': final_msg
                }, timeout=5)
            except:
                pass
                
    # Run in background to avoid blocking the UI
    threading.Thread(target=send_broadcast_background, args=(members, msg_template)).start()
    
    return jsonify({'status': 'success', 'message': f'Broadcast sedang dikirim ke {len(members)} anggota di latar belakang.'})

# Helper internal untuk notifikasi otomatis (struk dll)
def send_wa_notification(member_id, message):
    try:
        conn = database.get_db_connection()
        member = conn.execute("SELECT telepon FROM anggota WHERE member_id = ?", (member_id,)).fetchone()
        conn.close()
        
        if member and member['telepon']:
            import threading
            def _send():
                try:
                    requests.post('http://127.0.0.1:3000/api/send_message', json={
                        'number': member['telepon'],
                        'message': message
                    }, timeout=5)
                except:
                    pass
            threading.Thread(target=_send).start()
    except:
        pass

@app.route('/api/version', methods=['GET'])
def api_version():
    return jsonify({'version': '2b2fa3d-fix-401', 'status': 'ok'})
