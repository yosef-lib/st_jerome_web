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
            INSERT INTO buku (
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
        conn.execute('INSERT INTO buku_dibaca (no_induk) VALUES (?)', (no_induk,))
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
    dominant_author = dominant_author_row['pengarang'] if dominant_author_row else "Tidak diketahui"
    
    dominant_title_row = conn.execute('SELECT judul, COUNT(*) as c FROM buku WHERE judul != "" AND lokasi = ? GROUP BY judul ORDER BY c DESC LIMIT 1', (lokasi,)).fetchone()
    dominant_title = dominant_title_row['judul'] if dominant_title_row else "Tidak diketahui"
    
    # Koleksi Terbaru
    recent_books = conn.execute('SELECT no_induk, judul, pengarang FROM buku WHERE lokasi = ? ORDER BY id DESC LIMIT 5', (lokasi,)).fetchall()
    
    # Buku Sering Dibaca
    top_read_books = conn.execute('''
        SELECT b.no_induk, b.judul, b.pengarang, COUNT(bd.id) as read_count 
        FROM buku_dibaca bd 
        JOIN buku b ON bd.no_induk = b.no_induk 
        WHERE b.lokasi = ? 
        GROUP BY b.no_induk 
        ORDER BY read_count DESC 
        LIMIT 5
    ''', (lokasi,)).fetchall()
    
    pop_subject = "Ilmu Sosial (300)"
    if labels:
        pop_subject = f"Kelas DDC {labels[0]}"
        
    conn.close()
    
    return render_template('intelijen_evaluasi.html', 
                           total_buku=total_buku, 
                           lokasi=lokasi,
                           total_baca=total_baca, 
                           labels=labels, 
                           data_counts=data_counts,
                           dominant_author=dominant_author,
                           dominant_title=dominant_title,
                           recent_books=recent_books,
                           top_read_books=top_read_books,
                           pop_subject=pop_subject)

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
