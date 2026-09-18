import sqlite3
import os

DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'katalog.db')

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Master Koleksi Terpadu
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS buku (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        no_induk TEXT UNIQUE NOT NULL,
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
        copy_ke INTEGER DEFAULT 1,
        catatan TEXT,
        pengarang TEXT,
        subjek TEXT,
        status_buku TEXT DEFAULT 'BELI',
        lokasi TEXT DEFAULT 'IMAVI',
        tgl_terima TEXT
    )
    ''')

    # 2. Pencatatan Keterbacaan Harian (Hasil Pindai Kamera Ponsel)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS buku_dibaca (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        no_induk TEXT NOT NULL,
        waktu_baca DATETIME DEFAULT CURRENT_TIMESTAMP,
        tanggal DATE DEFAULT (DATE('now', 'localtime')),
        FOREIGN KEY (no_induk) REFERENCES buku(no_induk)
    )
    ''')

    # 3. Rekapitulasi Evaluasi Semesteran (Arsip 6 Bulanan)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS evaluasi_semester (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        periode_label TEXT NOT NULL,       
        tgl_evaluasi DATE NOT NULL,
        total_koleksi_imavi INTEGER,
        total_baca_inhouse INTEGER,
        subjek_terpopuler TEXT,            
        subjek_defisit TEXT,               
        laporan_narasi_ai TEXT             
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    print("Membaca dan menginisialisasi database...")
    init_db()
    print("Database berhasil diinisialisasi.")
