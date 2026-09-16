import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

# I will replace the current /import_slims POST logic
old_import = '''@app.route('/import_slims', methods=['GET', 'POST'])
@login_required
def import_slims():
    if request.method == 'POST':
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
                
                # Buat tabel jika belum ada
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
                # Hapus data lama agar terganti yang baru
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
                return "<script>alert('Sukses sinkronisasi data SLiMS!'); window.location.href='/analisis_lanjutan?lokasi=IMAVI';</script>"
            except Exception as e:
                return f"Error memproses file: {str(e)}", 500
                
    return render_template('import_slims.html')'''

new_import = '''@app.route('/import_slims', methods=['GET'])
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
        
        df_biblio = pd.read_csv(biblio_path, dtype=str)
        df_item = pd.read_csv(item_path, dtype=str)
        
        # Merge logic
        if 'title' in df_biblio.columns and 'biblio_id' in df_item.columns:
            df = pd.merge(df_item, df_biblio, on='biblio_id', how='left')
        elif 'Judul' in df_biblio.columns and 'ID Bibliografi' in df_item.columns:
            df = pd.merge(df_item, df_biblio, left_on='ID Bibliografi', right_on='ID Bibliografi', how='left')
        else:
            bib_id_col = next((c for c in df_biblio.columns if 'id' in c.lower()), None)
            item_bib_id_col = next((c for c in df_item.columns if 'biblio' in c.lower() and 'id' in c.lower()), None)
            df = pd.merge(df_item, df_biblio, left_on=item_bib_id_col, right_on=bib_id_col, how='left')
            
        conn = database.get_db_connection()
        conn.execute('DELETE FROM buku')
        
        count = 0
        for _, row in df.iterrows():
            def get_val(cols):
                for c in cols:
                    if c in row and pd.notna(row[c]):
                        return str(row[c]).strip()
                return ''
                
            no_induk = get_val(['item_code', 'Kode Eksemplar', 'nomor_induk'])
            if not no_induk: continue
            
            judul = get_val(['title', 'Judul'])
            pengarang = get_val(['author', 'Pengarang'])
            lokasi = get_val(['location_name', 'Lokasi', 'lokasi'])
            klasifikasi = get_val(['classification', 'Klasifikasi'])
            subjek = get_val(['subject', 'Subjek'])
            
            gmd = get_val(['gmd_name', 'GMD'])
            edisi = get_val(['edition', 'Edisi'])
            isbn = get_val(['isbn_issn', 'ISBN/ISSN'])
            penerbit = get_val(['publisher_name', 'Penerbit'])
            tahun_terbit = get_val(['publish_year', 'Tahun Terbit'])
            tempat_terbit = get_val(['publish_place', 'Tempat Terbit'])
            deskripsi = get_val(['collation', 'Deskripsi Fisik'])
            status_buku = get_val(['item_status_name', 'Status'])
            tgl_terima = get_val(['received_date', 'Tanggal Terima'])
            
            # Use call_number from item if exists, otherwise fallback to parsing from classification
            # We will save call_number into classification, cutter, huruf_judul logic or directly if no_panggil existed.
            # But wait! Our DB schema doesn't have no_panggil! We fixed the SQL by concatenating klasifikasi, cutter, huruf_judul.
            # So we must parse the call_number back into klasifikasi, cutter, huruf_judul!
            call_number = get_val(['call_number', 'Nomor Panggil'])
            parts = call_number.split(' ') if call_number else []
            
            # If call number is present on item, override the biblio classification
            final_class = parts[0] if len(parts) > 0 else klasifikasi
            cutter = parts[1] if len(parts) > 1 else get_val(['classification_cutter', 'Cutter'])
            huruf = parts[2] if len(parts) > 2 else ''
            
            conn.execute("""
                INSERT INTO buku (no_induk, judul, pengarang, lokasi, klasifikasi, cutter, huruf_judul, subjek,
                                gmd, edisi, isbn, penerbit, tahun_terbit, tempat_terbit, 
                                deskripsi_fisik, status_buku, tgl_terima)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (no_induk, judul, pengarang, lokasi, final_class, cutter, huruf, subjek,
                  gmd, edisi, isbn, penerbit, tahun_terbit, tempat_terbit, 
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
        return f"Error memproses file: {str(e)}", 500'''

app_code = app_code.replace(old_import, new_import)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)

print("App.py updated")

# Now update the UI
with codecs.open('templates/import_slims.html', 'r', 'utf-8') as f:
    html = f.read()

new_html = '''{% extends 'layout.html' %}

{% block page_title %}Sinkronisasi Data SLiMS{% endblock %}
{% block page_subtitle %}Unggah Data Ekspor SLiMS Anda ke St. Jerome{% endblock %}

{% block content %}
<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
    
    <!-- Upload Katalog (Biblio & Item) -->
    <div class="rounded-sm border border-stroke bg-white shadow-default p-6 text-center">
        <div class="mb-4 inline-flex h-16 w-16 items-center justify-center rounded-full bg-primary/10 text-primary">
            <i class="fa-solid fa-book text-3xl"></i>
        </div>
        <h2 class="text-xl font-bold text-black mb-2">1. Sinkronisasi Katalog Buku</h2>
        <p class="text-sm text-slate-600 mb-6">Wajib dilakukan untuk <strong>Audit Rak</strong>, <strong>Akreditasi</strong>, dan mencetak stiker. Pastikan format CSV dengan pembatas koma (,) dan header dicentang.</p>
        
        <form action="/import_slims_katalog" method="POST" enctype="multipart/form-data" class="flex flex-col gap-4 text-left">
            <div>
                <label class="mb-2 block text-sm font-medium text-black">File Daftar Judul (biblio.csv)</label>
                <input type="file" name="biblio_file" accept=".csv" required
                    class="w-full cursor-pointer rounded border-[1.5px] border-stroke bg-transparent font-medium outline-none transition file:mr-4 file:border-0 file:bg-gray-2 file:py-2 file:px-4 file:hover:bg-primary file:hover:text-white focus:border-primary active:border-primary" />
            </div>
            
            <div>
                <label class="mb-2 block text-sm font-medium text-black">File Daftar Fisik (item.csv)</label>
                <input type="file" name="item_file" accept=".csv" required
                    class="w-full cursor-pointer rounded border-[1.5px] border-stroke bg-transparent font-medium outline-none transition file:mr-4 file:border-0 file:bg-gray-2 file:py-2 file:px-4 file:hover:bg-primary file:hover:text-white focus:border-primary active:border-primary" />
            </div>
            
            <button type="submit" class="mt-2 inline-flex w-full items-center justify-center gap-2 rounded bg-primary py-2.5 px-6 font-medium text-white hover:bg-opacity-90 transition">
                <i class="fa-solid fa-upload"></i> Unggah & Proses
            </button>
        </form>
    </div>
    
    <!-- Upload Peminjaman -->
    <div class="rounded-sm border border-stroke bg-white shadow-default p-6 text-center">
        <div class="mb-4 inline-flex h-16 w-16 items-center justify-center rounded-full bg-success/10 text-success">
            <i class="fa-solid fa-users text-3xl"></i>
        </div>
        <h2 class="text-xl font-bold text-black mb-2">2. Sinkronisasi Peminjaman</h2>
        <p class="text-sm text-slate-600 mb-6">Wajib dilakukan untuk <strong>Dashboard</strong>, <strong>Turnover Rate</strong>, dan memantau <strong>Buku Dorman</strong>. Ekspor riwayat peminjaman SLiMS Anda sebagai Excel (.xlsx).</p>
        
        <form action="/import_slims_loan" method="POST" enctype="multipart/form-data" class="flex flex-col gap-4 text-left h-full">
            <div>
                <label class="mb-2 block text-sm font-medium text-black">File Laporan Peminjaman (.xlsx)</label>
                <input type="file" name="file" accept=".xlsx, .xls" required
                    class="w-full cursor-pointer rounded border-[1.5px] border-stroke bg-transparent font-medium outline-none transition file:mr-4 file:border-0 file:bg-gray-2 file:py-2 file:px-4 file:hover:bg-success file:hover:text-white focus:border-success active:border-success" />
            </div>
            
            <div class="flex-grow"></div>
            
            <button type="submit" class="mt-2 inline-flex w-full items-center justify-center gap-2 rounded bg-success py-2.5 px-6 font-medium text-white hover:bg-opacity-90 transition">
                <i class="fa-solid fa-upload"></i> Unggah & Proses
            </button>
        </form>
    </div>
    
</div>
{% endblock %}
'''

with codecs.open('templates/import_slims.html', 'w', 'utf-8') as f:
    f.write(new_html)

print("UI updated")
